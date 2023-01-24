#!/usr/bin/python
# coding=utf-8
import datetime
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

# Initiate clients
date = datetime.datetime.now()
date = date.strftime('%a %b %d')

SENDER = 'piepiesw@amazon.com'

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

SUBJECT = '[Amazon Highlights] Weekly Digest - ' + date

# The character encoding for the email.
CHARSET = "UTF-8"
# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('User-uutjsp7nhrh67kfdb54ibsiug4-prod')
summary_table = dynamodb.Table('Summary')


# --------------- Main handler ------------------

def lambda_handler(event, context):
    response = 1
    try:
        users = user_table.scan(FilterExpression=Attr('__typename').eq('User'))
        # print(users['Items'])
        for user in users['Items']:
            contents = makeContent(user)
            print(contents)
            sendEmail(contents, user['name'], user['email'])
           
        return response

    except Exception as e:

        print(e)
        raise e


def makeContent(user):
    tags = user["tag"]
    summary=[]
    for tag in tags:
        cur = summary_table.scan(FilterExpression=Attr('keyword').eq(tag))
        if cur['Items']:
            summary.append(cur['Items'])
    return summary

# --------------- Helper Functions to call SES APIs ------------------

def sendEmail(contents, name, email):
    trs = []
    print(contents)
    for content in contents:
        trs.append(f"""
              <table
                class="es-content"
                cellspacing="0"
                cellpadding="0"
                align="center"
                style="
                  mso-table-lspace: 0pt;
                  mso-table-rspace: 0pt;
                  border-collapse: collapse;
                  border-spacing: 0px;
                  table-layout: fixed !important;
                  width: 100%;
                ">
                <tr style="border-collapse: collapse">
                  <td align="center" style="padding: 0; margin: 0">
                    <table
                      class="es-content-body"
                      cellspacing="0"
                      cellpadding="0"
                      bgcolor="#ffffff"
                      align="center"
                      style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        background-color: #ffffff;
                        width: 600px;
                      ">
                      <tr style="border-collapse: collapse">
                        <td align="left" style="padding: 0; margin: 0">
                          <table
                            width="100%"
                            cellspacing="0"
                            cellpadding="0"
                            style="
                              mso-table-lspace: 0pt;
                              mso-table-rspace: 0pt;
                              border-collapse: collapse;
                              border-spacing: 0px;
                            ">
                            <tr style="border-collapse: collapse">
                              <td
                                valign="top"
                                align="center"
                                style="padding: 0; margin: 0; width: 600px">
                                <table
                                  width="100%"
                                  cellspacing="0"
                                  cellpadding="0"
                                  role="presentation"
                                  style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                  ">
                                  <tr style="border-collapse: collapse">
                                    <td
                                      align="left"
                                      style="
                                        margin: 0;
                                        padding-bottom: 10px;
                                        padding-top: 20px;
                                        padding-left: 20px;
                                        padding-right: 20px;
                                      ">
                                      <h3
                                        style="
                                          margin: 0;
                                          line-height: 24px;
                                          mso-line-height-rule: exactly;
                                          font-family: helvetica, 'helvetica neue',
                                            arial, verdana, sans-serif;
                                          font-size: 20px;
                                          font-style: normal;
                                          font-weight: normal;
                                          color: #373a44;
                                        ">
                                        {content[0]['title']}
                                      </h3>
                                    </td>
                                  </tr>
                                  <tr style="border-collapse: collapse">
                                    <td
                                      class="es-m-txt-c"
                                      align="left"
                                      style="
                                        padding: 0;
                                        margin: 0;
                                        padding-left: 20px;
                                        padding-right: 20px;
                                      ">
                                      <p
                                        style="
                                          margin: 0;
                                          -webkit-text-size-adjust: none;
                                          -ms-text-size-adjust: none;
                                          mso-line-height-rule: exactly;
                                          font-family: helvetica, 'helvetica neue',
                                            arial, verdana, sans-serif;
                                          line-height: 21px;
                                          color: #999999;
                                          font-size: 14px;
                                        ">
                                        <span
                                          class="product-description"
                                          style="line-height: 150%"
                                          > {content[0]['summarization']}
                                        </span>
                                      </p>
                                    </td>
                                  </tr>
                                  <tr style="border-collapse: collapse">
                                    <td
                                      class="es-m-txt-c"
                                      align="left"
                                      style="
                                        margin: 0;
                                        padding-top: 10px;
                                        padding-bottom: 20px;
                                        padding-left: 20px;
                                        padding-right: 20px;
                                      ">
                                      <!--[if mso
                                        ]><a
                                          href="https://viewstripo.email"
                                          target="_blank"
                                          hidden>
                                          <v:roundrect
                                            xmlns:v="urn:schemas-microsoft-com:vml"
                                            xmlns:w="urn:schemas-microsoft-com:office:word"
                                            esdevVmlButton
                                            href="https://viewstripo.email"
                                            style="
                                              height: 24px;
                                              v-text-anchor: middle;
                                              width: 108px;
                                            "
                                            arcsize="0%"
                                            strokecolor="#333333"
                                            strokeweight="2px"
                                            fillcolor="#ffffff">
                                            <w:anchorlock></w:anchorlock>
                                            <center
                                              style="
                                                color: #292929;
                                                font-family: 'trebuchet ms',
                                                  'lucida grande',
                                                  'lucida sans unicode',
                                                  'lucida sans', tahoma,
                                                  sans-serif;
                                                font-size: 8px;
                                                font-weight: 700;
                                                line-height: 8px;
                                                mso-text-raise: 1px;
                                              ">
                                              Read more >
                                            </center>
                                          </v:roundrect></a
                                        ><!
                                      [endif]--><!--[if !mso]><!-- --><span
                                        class="es-button-border msohide"
                                        style="
                                          border-style: solid;
                                          border-color: #f1f1f1 #f1f1f1 #333333;
                                          background: #ffffff;
                                          border-width: 0px 0px 2px 0px;
                                          display: inline-block;
                                          border-radius: 0px;
                                          width: auto;
                                          mso-hide: all;
                                          border-bottom: 2px solid #333333;
                                        "
                                        ><a
                                          href="https://viewstripo.email"
                                          class="es-button es-button-1"
                                          target="_blank"
                                          style="
                                            -webkit-text-size-adjust: none;
                                            -ms-text-size-adjust: none;
                                            mso-line-height-rule: exactly;
                                            color: #292929;
                                            font-size: 16px;
                                            border-style: solid;
                                            border-color: #ffffff;
                                            border-width: 0px;
                                            display: inline-block;
                                            background: #ffffff;
                                            border-radius: 0px;
                                            font-family: 'trebuchet ms',
                                              'lucida grande',
                                              'lucida sans unicode', 'lucida sans',
                                              tahoma, sans-serif;
                                            font-weight: bold;
                                            font-style: italic;
                                            line-height: 19px;
                                            width: auto;
                                            text-align: center;
                                            text-decoration: none;
                                            mso-style-priority: 100;
                                          "
                                          >Read more &gt;<!--<![endif]--> </a
                                      ></span>
                                    </td>
                                  </tr>
                                </table>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
    """)
    table_contents = '\n'.join(trs)
    
    data_html = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:o="urn:schemas-microsoft-com:office:office"
  style="
    width: 100%;
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
    padding: 0;
    margin: 0;
  ">
  <head>
    <meta charset="UTF-8" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <meta name="x-apple-disable-message-reformatting" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta content="telephone=no" name="format-detection" />
    <title>Amazon Highlights</title>
    <!--[if (mso 16)]> <![endif]-->
    <!--[if gte mso 9
      ]><xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG></o:AllowPNG> <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
      </xml><!
    [endif]-->
  </head>
  <body
    style="
      width: 100%;
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
      font-family: helvetica, 'helvetica neue', arial, verdana, sans-serif;
      padding: 0;
      margin: 0;
    ">
    <div class="es-wrapper-color" style="background-color: #f6f6f6">
      <!--[if gte mso 9
        ]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
          <v:fill type="tile" color="#f6f6f6"></v:fill> </v:background
      ><![endif]-->
      <table
        class="es-wrapper"
        width="100%"
        cellspacing="0"
        cellpadding="0"
        style="
          mso-table-lspace: 0pt;
          mso-table-rspace: 0pt;
          border-collapse: collapse;
          border-spacing: 0px;
          padding: 0;
          margin: 0;
          width: 100%;
          height: 100%;
          background-repeat: repeat;
          background-position: center top;
          background-color: #f6f6f6;
        ">
        <tr style="border-collapse: collapse">
          <td valign="top" style="padding: 0; margin: 0">
            <table
              cellpadding="0"
              cellspacing="0"
              class="es-content"
              align="center"
              style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                table-layout: fixed !important;
                width: 100%;
              ">
              <tr style="border-collapse: collapse">
                <td
                  class="es-adaptive"
                  align="center"
                  style="padding: 0; margin: 0">
                  <table
                    class="es-content-body"
                    style="
                      mso-table-lspace: 0pt;
                      mso-table-rspace: 0pt;
                      border-collapse: collapse;
                      border-spacing: 0px;
                      background-color: transparent;
                      width: 600px;
                    "
                    cellspacing="0"
                    cellpadding="0"
                    align="center">
                    <tr style="border-collapse: collapse">
                      <td align="left" style="padding: 10px; margin: 0">
                        <table
                          width="100%"
                          cellspacing="0"
                          cellpadding="0"
                          style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                          ">
                          <tr style="border-collapse: collapse">
                            <td
                              valign="top"
                              align="center"
                              style="padding: 0; margin: 0; width: 580px">
                              <table
                                width="100%"
                                cellspacing="0"
                                cellpadding="0"
                                role="presentation"
                                style="
                                  mso-table-lspace: 0pt;
                                  mso-table-rspace: 0pt;
                                  border-collapse: collapse;
                                  border-spacing: 0px;
                                ">
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="center"
                                    class="es-infoblock"
                                    style="
                                      padding: 0;
                                      margin: 0;
                                      line-height: 14px;
                                      font-size: 12px;
                                      color: #cccccc;
                                    "></td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table
              cellpadding="0"
              cellspacing="0"
              class="es-header"
              align="center"
              style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                table-layout: fixed !important;
                width: 100%;
                background-color: transparent;
                background-repeat: repeat;
                background-position: center top;
              ">
              <tr style="border-collapse: collapse">
                <td align="center" style="padding: 0; margin: 0">
                  <table
                    class="es-header-body"
                    cellspacing="0"
                    cellpadding="0"
                    align="center"
                    style="
                      mso-table-lspace: 0pt;
                      mso-table-rspace: 0pt;
                      border-collapse: collapse;
                      border-spacing: 0px;
                      background-color: #ffffff;
                      width: 600px;
                    ">
                    <tr style="border-collapse: collapse">
                      <td
                        align="left"
                        style="
                          margin: 0;
                          padding-top: 10px;
                          padding-bottom: 10px;
                          padding-left: 10px;
                          padding-right: 10px;
                        ">
                        <!--[if mso]><table style="width:580px" cellpadding="0" cellspacing="0"><tr><td style="width:280px" valign="top"><![endif]-->
                        <table
                          class="es-left"
                          cellspacing="0"
                          cellpadding="0"
                          align="left"
                          style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            float: left;
                          ">
                          <tr style="border-collapse: collapse">
                            <td
                              class="es-m-p20b"
                              align="left"
                              style="padding: 0; margin: 0; width: 280px">
                              <table
                                width="100%"
                                cellspacing="0"
                                cellpadding="0"
                                role="presentation"
                                style="
                                  mso-table-lspace: 0pt;
                                  mso-table-rspace: 0pt;
                                  border-collapse: collapse;
                                  border-spacing: 0px;
                                ">
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="left"
                                    style="
                                      padding: 0;
                                      margin: 0;
                                      font-size: 0px;
                                    ">
                                    <a
                                      href="https://prod.d1ab0xvhc27cvp.amplifyapp.com/"
                                      target="_blank"
                                      style="
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        text-decoration: underline;
                                        color: #bca76e;
                                        font-size: 14px;
                                      "
                                      ><img
                                        src="https://i.postimg.cc/5yPFc6SK/AH-LOGO.png"
                                        alt="Amazon Highlights"
                                        title="Amazon Highlights"
                                        width="165"
                                        style="
                                          display: block;
                                          border: 0;
                                          outline: none;
                                          text-decoration: none;
                                          -ms-interpolation-mode: bicubic;
                                        "
                                        height="61"
                                    /></a>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso]></td><td style="width:20px"></td><td style="width:280px" valign="top"><![endif]-->
                        <table
                          class="es-right"
                          cellspacing="0"
                          cellpadding="0"
                          align="right"
                          style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            float: right;
                          ">
                          <tr style="border-collapse: collapse">
                            <td
                              align="left"
                              style="padding: 0; margin: 0; width: 280px">
                              <table
                                width="100%"
                                cellspacing="0"
                                cellpadding="0"
                                role="presentation"
                                style="
                                  mso-table-lspace: 0pt;
                                  mso-table-rspace: 0pt;
                                  border-collapse: collapse;
                                  border-spacing: 0px;
                                ">
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="right"
                                    style="
                                      padding: 0;
                                      margin: 0;
                                      padding-top: 10px;
                                    ">
                                    <p
                                      style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        line-height: 21px;
                                        color: #373a44;
                                        font-size: 14px;
                                      ">
                                      <br />
                                    </p>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso]></td>
</tr></table><![endif]-->
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table
              class="es-content"
              cellspacing="0"
              cellpadding="0"
              align="center"
              style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                table-layout: fixed !important;
                width: 100%;
              ">
              <tr style="border-collapse: collapse">
                <td align="center" style="padding: 0; margin: 0">
                  <table
                    class="es-content-body"
                    cellspacing="0"
                    cellpadding="0"
                    bgcolor="#ffffff"
                    align="center"
                    style="
                      mso-table-lspace: 0pt;
                      mso-table-rspace: 0pt;
                      border-collapse: collapse;
                      border-spacing: 0px;
                      background-color: #ffffff;
                      width: 600px;
                    ">
                    <tr style="border-collapse: collapse">
                      <td
                        style="padding: 0; margin: 0; background-color: #373a44"
                        bgcolor="#373a44"
                        align="left">
                        <table
                          width="100%"
                          cellspacing="0"
                          cellpadding="0"
                          style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                          ">
                          <tr style="border-collapse: collapse">
                            <td
                              valign="top"
                              align="center"
                              style="padding: 0; margin: 0; width: 600px">
                              <table
                                style="
                                  mso-table-lspace: 0pt;
                                  mso-table-rspace: 0pt;
                                  border-collapse: separate;
                                  border-spacing: 0px;
                                  border-left: 6px solid #bca76e;
                                  border-right: 0px solid transparent;
                                  border-top: 0px solid transparent;
                                  border-bottom: 0px solid transparent;
                                "
                                width="100%"
                                cellspacing="0"
                                cellpadding="0"
                                role="presentation">
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="left"
                                    style="padding: 20px; margin: 0">
                                    <h1
                                      style="
                                        margin: 0;
                                        line-height: 36px;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        font-size: 30px;
                                        font-style: normal;
                                        font-weight: normal;
                                        color: #ffffff;
                                      ">
                                      What's new?
                                    </h1>
                                    <p
                                      style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        line-height: 21px;
                                        color: #ffffff;
                                        font-size: 14px;
                                      ">
                                      A weekly digest of interesting content.
                                    </p>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            {table_contents}
            <table
              cellpadding="0"
              cellspacing="0"
              class="es-footer"
              align="center"
              style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                table-layout: fixed !important;
                width: 100%;
                background-color: transparent;
                background-repeat: repeat;
                background-position: center top;
              ">
              <tr style="border-collapse: collapse">
                <td align="center" style="padding: 0; margin: 0">
                  <table
                    class="es-footer-body"
                    style="
                      mso-table-lspace: 0pt;
                      mso-table-rspace: 0pt;
                      border-collapse: collapse;
                      border-spacing: 0px;
                      background-color: #373a44;
                      width: 600px;
                    "
                    cellspacing="0"
                    cellpadding="0"
                    bgcolor="#373a44"
                    align="center">
                    <tr style="border-collapse: collapse">
                      <td
                        style="
                          margin: 0;
                          padding-top: 20px;
                          padding-bottom: 20px;
                          padding-left: 20px;
                          padding-right: 20px;
                          background-color: #373a44;
                        "
                        bgcolor="#373a44"
                        align="left">
                        <!--[if mso]><table style="width:560px" cellpadding="0" cellspacing="0"><tr><td style="width:270px" valign="top"><![endif]-->
                        <table
                          class="es-left"
                          cellspacing="0"
                          cellpadding="0"
                          align="left"
                          style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            float: left;
                          ">
                          <tr style="border-collapse: collapse">
                            <td
                              class="es-m-p20b"
                              align="left"
                              style="padding: 0; margin: 0; width: 270px">
                              <table
                                width="100%"
                                cellspacing="0"
                                cellpadding="0"
                                role="presentation"
                                style="
                                  mso-table-lspace: 0pt;
                                  mso-table-rspace: 0pt;
                                  border-collapse: collapse;
                                  border-spacing: 0px;
                                ">
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="left"
                                    style="padding: 0; margin: 0">
                                    <h3
                                      style="
                                        margin: 0;
                                        line-height: 24px;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        font-size: 20px;
                                        font-style: normal;
                                        font-weight: normal;
                                        color: #ffffff;
                                      ">
                                      Contact Us
                                    </h3>
                                  </td>
                                </tr>
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="left"
                                    style="
                                      padding: 0;
                                      margin: 0;
                                      padding-top: 10px;
                                    ">
                                    <p
                                      style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        line-height: 21px;
                                        color: #ffffff;
                                        font-size: 14px;
                                      ">
                                      Tech U 2022 syd cohort<br />Team
                                      ChoChoChoi<br />Andy Cho (chhyu@)<br />Bailey
                                      Cho (csbailey@)<br />Seungwon Choi
                                      (piepiesw@)<br />
                                    </p>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso]></td><td style="width:20px"></td>
<td style="width:270px" valign="top"><![endif]-->
                        <table
                          class="es-right"
                          cellspacing="0"
                          cellpadding="0"
                          align="right"
                          style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            float: right;
                          ">
                          <tr style="border-collapse: collapse">
                            <td
                              align="left"
                              style="padding: 0; margin: 0; width: 270px">
                              <table
                                width="100%"
                                cellspacing="0"
                                cellpadding="0"
                                role="presentation"
                                style="
                                  mso-table-lspace: 0pt;
                                  mso-table-rspace: 0pt;
                                  border-collapse: collapse;
                                  border-spacing: 0px;
                                ">
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="left"
                                    style="
                                      padding: 0;
                                      margin: 0;
                                      padding-top: 25px;
                                    ">
                                    <p
                                      style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        line-height: 21px;
                                        color: #ffffff;
                                        font-size: 14px;
                                      ">
                                      You are receiving this email because you
                                      have visited our site or asked us about
                                      regular newsletter.<br />
                                    </p>
                                  </td>
                                </tr>
                                <tr style="border-collapse: collapse">
                                  <td
                                    align="left"
                                    style="
                                      padding: 0;
                                      margin: 0;
                                      padding-top: 25px;
                                    ">
                                    <p
                                      style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        line-height: 21px;
                                        color: #ffffff;
                                        font-size: 14px;
                                      ">
                                      If you wish to unsubscribe from our
                                      newsletter, click
                                      <a
                                        target="_blank"
                                        class="unsubscribe"
                                        href=""
                                        style="
                                          -webkit-text-size-adjust: none;
                                          -ms-text-size-adjust: none;
                                          mso-line-height-rule: exactly;
                                          text-decoration: underline;
                                          color: #ffffff;
                                          font-size: 14px;
                                        "
                                        >here.
                                      </a>
                                    </p>
                                    <p
                                      style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: helvetica, 'helvetica neue',
                                          arial, verdana, sans-serif;
                                        line-height: 21px;
                                        color: #ffffff;
                                        font-size: 14px;
                                      ">
                                      © 2023
                                    </p>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>
                        <!--[if mso]></td></tr></table><![endif]-->
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </div>
  </body>
</html>
    """
    
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': data_html,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])