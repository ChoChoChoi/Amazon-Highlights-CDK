import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as fs from 'fs';

import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as s3n from "aws-cdk-lib/aws-s3-notifications";
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';

export class AmazonHighlightsCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //bucket for storing contents
    const contentsBucket = new s3.Bucket(this, "contentsBucket");

    //lambdas
    const getContentsLambda = new lambda.Function(this, 'DetectLambda', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/getContents.py', { encoding: 'utf-8' })),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment: {
      }
    });

    const getScriptLambda = new lambda.Function(this, 'DetectLambda', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/getScript.py', { encoding: 'utf-8' })),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment: {
      }
    });

    const getSummaryLambda = new lambda.Function(this, 'DetectLambda', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/getSummary.py', { encoding: 'utf-8' })),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment: {
      }
    });

    const putResultLambda = new lambda.Function(this, 'DetectLambda', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/putResult.py', { encoding: 'utf-8' })),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment: {
      }
    });

    const sendEmailLambda = new lambda.Function(this, 'DetectLambda', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/sendEmail.py', { encoding: 'utf-8' })),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment: {
      }
    });

    //step function definition
    const getScript = new tasks.LambdaInvoke(this, 'detectAnomaliesLambda', { lambdaFunction: getScriptLambda, outputPath: '$.Payload' });
    const getSummary = new tasks.LambdaInvoke(this, 'ClassifyDefects', { lambdaFunction: getSummaryLambda, outputPath: '$.Payload' });
    const putResult = new tasks.LambdaInvoke(this, 'putResult', { lambdaFunction: putResultLambda, outputPath: '$.Payload' });

    //create chain
    // const choice = new sfn.Choice(this,'IsAnomaly?');
    // const skip = new sfn.Pass(this, 'pass');
    // choice.when(sfn.Condition.booleanEquals('$.DetectAnomalyResult.IsAnomalous',true), classifyDefects);
    // choice.when(sfn.Condition.booleanEquals('$.DetectAnomalyResult.IsAnomalous',false), skip);
    // choice.afterwards().next(putResult);
    // const definition = DetectAnomalies.next(choice);

    //create state machine
    const stateMachine = new sfn.StateMachine(this, 'stateMachine', {definition, timeout: cdk.Duration.minutes(5)});

    const startStateMachineLambda = new lambda.Function(this, 'startLambda', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/DetectAnomaliesFunction/startStateMachineExecution.py', { encoding: 'utf-8' })),
      handler: 'index.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      runtime: lambda.Runtime.PYTHON_3_9,
      environment: {
        STATE_MACHINE_ARN : stateMachine.stateMachineArn
      }
    });
    
  }
}
