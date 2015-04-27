import flask.ext.mail
from flask import g, app
import r

def send(subject: str, recipients: list, plaintext: str, html: str):
    message = flask.ext.mail.Message(
        subject=subject,
        recipients=recipients,
        sender=('Review', 'noreply@letsreview.io'),
        body=plaintext,
        html=layout % html
    )

    # just print emails in debug mode
    if app.debug:
        print(plaintext)
        return

    r.mailer.send(message)

layout = """
<table width="100%%" bgcolor="#FAFAFA">
    <tr>
        <td class="spacing" colspan="3" height="40">
    </tr>
    <tr>
        <td>
            <table align="center" cellspacing="0" cellpadding="0" border="0" bgcolor="#FFFFFF" width="600" style="font-weight:normal; font-size:1em; line-height:1.2em; font-family:Helvetica Neue, HelveticaNeue, Helvetica, sans-serif, Arial !important">
                <tr>
                    <td colspan="3">
                        <table cellpadding="0" cellspacing="0" width="600">
                            <tr>
                                <td width="3" height="1" colspan="3" bgcolor="#FAFAFA"></td>
                                <td width="1" height="1" bgcolor="#F8F8F8"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#F5F5F5"></td>
                                <td width="1" height="1" bgcolor="#F3F3F3"></td>
                                <td width="586" bgcolor="#F0F0F0"></td>
                                <td width="1" height="1" bgcolor="#F3F3F3"></td>
                                <td width="1" height="1" bgcolor="#F5F5F5"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#F8F8F8"></td>
                                <td width="3" height="1" colspan="3" bgcolor="#FAFAFA"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#F2F2F2"></td>
                                <td width="1" height="1" bgcolor="#EEEEEE"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#FCFCFC"></td>
                                <td width="586" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#FCFCFC"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#EEEEEE"></td>
                                <td width="1" height="1" bgcolor="#F2F2F2"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#EFEFEF"></td>
                                <td width="1" height="1" bgcolor="#F0F0F0"></td>
                                <td width="1" height="1" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#FFFFFF"></td>
                                <td width="586" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#F0F0F0"></td>
                                <td width="1" height="1" bgcolor="#EFEFEF"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#EFEFEF"></td>
                                <td width="1" height="1" bgcolor="#F0F0F0"></td>
                                <td width="592" height="1" colspan="7" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#F0F0F0"></td>
                                <td width="1" height="1" bgcolor="#EFEFEF"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#F3F3F3"></td>
                                <td width="594" height="1" colspan="9" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#F3F3F3"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#F5F5F5"></td>
                                <td width="1" height="1" bgcolor="#E1E1E1"></td>
                                <td width="1" height="1" bgcolor="#FBFBFB"></td>
                                <td width="594" height="1" colspan="9" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#FBFBFB"></td>
                                <td width="1" height="1" bgcolor="#E1E1E1"></td>
                                <td width="1" height="1" bgcolor="#F5F5F5"></td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td colspan="3">
                        <table cellpadding="0" cellspacing="0" width="600">
                            <tr>
                                <td width="1" bgcolor="#F0F0F0">
                                </td>
                                <td width="1" bgcolor="#D5D5D5">
                                </td>
                                <td>
                                    <table>
                                        <tr class="header">
                                            <td width="20"></td>
                                            <td width="560"><h1 style="font-size: 24px; line-height: 50px; margin-bottom: 0px; border-bottom: 1px solid #DDD; font-family:Helvetica Neue, HelveticaNeue, Helvetica, sans-serif, Arial">
                                                Let's Review.
                                            </h1></td>
                                            <td width="20"></td>
                                        </tr>
                                        <tr>
                                            <td class="spacing" colspan="3" height="10">
                                        </tr>
                                        <tr class="content">
                                            <td width="560" colspan="3">
                                                <table>
                                                    <td width="25"></td>
                                                    <td width="510" style="font-size: 14px; line-height: 1.2em; font-family:Helvetica Neue, HelveticaNeue, Helvetica, sans-serif, Arial;">
                                                        %s
                                                    </td>
                                                    <td width="25"></td>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="spacing" colspan="3" height="20">
                                        </tr>
                                    </table>
                                </td>
                                <td width="1" bgcolor="#D5D5D5">
                                </td>
                                <td width="1" bgcolor="#F0F0F0">
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td colspan="3">
                        <table cellpadding="0" cellspacing="0" width="600">
                            <tr>
                                <td width="1" height="1" bgcolor="#F3F3F3"></td>
                                <td width="1" height="1" bgcolor="#D9D9D9"></td>
                                <td width="1" height="1" bgcolor="#EDEDED"></td>
                                <td width="594" height="1" colspan="9" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#EDEDED"></td>
                                <td width="1" height="1" bgcolor="#D9D9D9"></td>
                                <td width="1" height="1" bgcolor="#F3F3F3"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#F5F5F5"></td>
                                <td width="1" height="1" bgcolor="#E1E1E1"></td>
                                <td width="1" height="1" bgcolor="#D3D3D3"></td>
                                <td width="594" height="1" colspan="9" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#D3D3D3"></td>
                                <td width="1" height="1" bgcolor="#E1E1E1"></td>
                                <td width="1" height="1" bgcolor="#F5F5F5"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#D3D3D3"></td>
                                <td width="1" height="1" bgcolor="#DADADA"></td>
                                <td width="592" height="1" colspan="7" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#DADADA"></td>
                                <td width="1" height="1" bgcolor="#D3D3D3"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                                <td width="1" height="1" bgcolor="#F2F2F2"></td>
                                <td width="1" height="1" bgcolor="#E3E3E3"></td>
                                <td width="1" height="1" bgcolor="#D0D0D0"></td>
                                <td width="1" height="1" bgcolor="#C9C9C9"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                                <td width="586" bgcolor="#FFFFFF"></td>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#C9C9C9"></td>
                                <td width="1" height="1" bgcolor="#D0D0D0"></td>
                                <td width="1" height="1" bgcolor="#E3E3E3"></td>
                                <td width="1" height="1" bgcolor="#F2F2F2"></td>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#EFEFEF"></td>
                                <td width="1" height="1" bgcolor="#E3E3E3"></td>
                                <td width="1" height="1" bgcolor="#D3D3D3"></td>
                                <td width="1" height="1" bgcolor="#C6C6C6"></td>
                                <td width="1" height="1" bgcolor="#BFBFBF"></td>
                                <td width="586" bgcolor="#BBBBBB"></td>
                                <td width="1" height="1" bgcolor="#BFBFBF"></td>
                                <td width="1" height="1" bgcolor="#C6C6C6"></td>
                                <td width="1" height="1" bgcolor="#D3D3D3"></td>
                                <td width="1" height="1" bgcolor="#E3E3E3"></td>
                                <td width="1" height="1" bgcolor="#EFEFEF"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                            </tr>
                            <tr>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#F2F2F2"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#E0E0E0"></td>
                                <td width="1" height="1" bgcolor="#D9D9D9"></td>
                                <td width="586" bgcolor="#D5D5D5"></td>
                                <td width="1" height="1" bgcolor="#D9D9D9"></td>
                                <td width="1" height="1" bgcolor="#E0E0E0"></td>
                                <td width="1" height="1" bgcolor="#EAEAEA"></td>
                                <td width="1" height="1" bgcolor="#F2F2F2"></td>
                                <td width="1" height="1" bgcolor="#F7F7F7"></td>
                                <td width="1" height="1" bgcolor="#F9F9F9"></td>
                                <td width="1" height="1" bgcolor="#FAFAFA"></td>
                            </tr>
                            <tr>
                                <td width="7" colspan="7" height="1" bgcolor="#FAFAFA"></td>
                                <td width="586" bgcolor="#F0F0F0"></td>
                                <td width="7" colspan="7" height="1" bgcolor="#FAFAFA"></td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td class="spacing" colspan="3" height="40">
    </tr>
<table>
"""
