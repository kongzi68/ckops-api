# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import logging
import requests #需要先使用pip install requests命令安装依赖
import time
import uuid
from . import api
from .api_auth import multi_auth
from ..auth.users import json_msg
from flask import request

logger = logging.getLogger(__name__)

#必填,请参考"开发准备-申请资源"获取如下数据,替换为实际值
base_url = 'https://rtccall.cn-north-1.myhuaweicloud.cn:443'#APP接入地址,购买服务时下发,请替换为实际值
appKey = '1H8OQEplciamIPaddrln27Hfhb'#语音通知应用的appKey,购买服务时下发,请替换为实际值
appSecret = 'jIr2euiamIPaddrCt1pqBuzQ'#语音通知应用的appSecret,购买服务时下发,请替换为实际值

def buildWSSEHeader(appKey, appSecret):
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ') #Created
    nonce = str(uuid.uuid4()).replace('-', '') #Nonce
    digest = hashlib.sha256((nonce + now + appSecret).encode()).hexdigest()
    digestBase64 = base64.b64encode(digest.encode()).decode() #PasswordDigest
    return 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}"'.format(appKey, digestBase64, nonce, now);

def voiceNotifyAPI(displayNbr, calleeNbr, playInfoList):
    if len(displayNbr) < 1 or len(calleeNbr) < 1 or playInfoList is None:
        return

    apiUri = '/rest/httpsessions/callnotify/v2.0' #v1.0 or v2.0
    requestUrl = base_url + apiUri

    header = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
        'X-WSSE': buildWSSEHeader(appKey, appSecret)
    }

    jsonData = {
        # 必填参数
        'displayNbr': displayNbr,#主叫用户手机终端的来电显示号码。
        'calleeNbr': calleeNbr,#发起呼叫时所拨打的被叫号码。
        'playInfoList': playInfoList#播放信息列表，最大支持5个，每个播放信息携带的参数都可以不相同。
        # 选填参数
        # 'statusUrl': '', #设置SP接收状态上报的URL,要求使用BASE64编码
        # 'feeUrl': '', #设置SP接收话单上报的URL,要求使用BASE64编码
        # 'returnIdlePort': 'false', #指示是否需要返回平台空闲呼叫端口数量
        # 'userData': 'customerId123' #设置用户的附属信息
    }

    try:
        r = requests.post(requestUrl, json=jsonData, headers=header, verify=False)
        # {"resultcode":"iamIPaddr","resultdesc":"Invalid request.The number format is incorrect."}
        logger.info(r.text) #打印响应结果
        return json.loads(r.text)
    except requests.exceptions.HTTPError as e:
        logger.error(e.code)
        logger.error(e.read().decode('utf-8')) #打印错误信息
        return {"resultcode": e.code, "resultdesc": e.read().decode('utf-8')}

def getPlayInfoList(templateId, templateParas):
    """
    模板ID：2babeiamIPaddrbbaaa14cc2057afefd
    模板内容：提醒：${TXT_32}环境，出现${TXT_32}，请及时处理。
    """
    playInfoList = [{
        # 'notifyVoice': notifyVoice,
        'templateId': templateId,
        'templateParas': templateParas
        # 'collectInd': 0, #是否进行收号
        # 'replayAfterCollection': 'false', #设置是否在收号后重新播放notifyVoice或templateId指定的放音
        # 'collectContentTriggerReplaying': '1' #设置触发重新放音的收号内容
    }]
    return playInfoList

@api.route('/call_phone', methods=['POST'])
@multi_auth.login_required
def callPhone():
    """拨打电话接口
    callee_nbr：电话号码，比如手机号码11位：iamIPaddr，不需要加上：+86，传入参数为：iamIPaddr
    send_txt：字符串，8个以内，比如：”wind消息告警“，中英文字符一共8个；“国泰安客户端故障”，8个中文字符
              这个字符的长度，与模板内容定义有关，比如：注意。服务器数据未更新。请及时处理${TXT_8}
              TXT_8，表示最大8个字符
    """
    if request.json:
        logger.debug('request.json：{0}'.format(request.json))
        ret_params = json.loads(request.json)
        callee_nbr = ret_params.get('callee_nbr', None)
        send_txt = ret_params.get('send_txt', None)
    else:
        logger.debug('request.values：{0}'.format(request.values))
        callee_nbr = request.values.get('callee_nbr', None)
        send_txt = request.values.get('send_txt', None)
    logger.debug('电话号码：{0}，告警信息：{1}'.format(callee_nbr, send_txt))
    # exit()
    if not send_txt:
        return json_msg(400, '语音消息字符串为空')
    elif send_txt.__len__() > 8:
        return json_msg(400, '传入的语音消息字符串长度不能大于8')
    if not callee_nbr:
        return json_msg(400, '电话号码为空')

    phone_nbr = '+86{0}'.format(callee_nbr)
    playInfoList = getPlayInfoList('BeiFa_MD_01', [send_txt])
    ret = voiceNotifyAPI('+iamIPaddr', phone_nbr, playInfoList)
    # resultcode，只有 0 表示成功，其余均为失败，iamIPaddr 表示号码填写不合法
    if int(ret.get("resultcode", iamIPaddr)) == 0:
        return json_msg(200, '拨打电话成功')
    else:
        return json_msg(400, '拨打电话失败')

@api.route('/call_phone_devops', methods=['POST'])
@multi_auth.login_required
def callPhoneNew():
    """拨打电话接口
    callee_nbr：电话号码，比如手机号码11位：iamIPaddr，不需要加上：+86，传入参数为：iamIPaddr
    send_txt：字符串，8个以内，比如：”wind消息告警“，中英文字符一共8个；“国泰安客户端故障”，8个中文字符
              这个字符的长度，与模板内容定义有关，比如：注意。服务器数据未更新。请及时处理${TXT_8}
              TXT_8，表示最大8个字符
    """
    if request.json:
        logger.debug('request.json：{0}'.format(request.json))
        ret_params = json.loads(request.json)
        callee_nbr = ret_params.get('callee_nbr', None)
        send_txt = ret_params.get('send_txt', None)
    else:
        logger.debug('request.values：{0}'.format(request.values))
        callee_nbr = request.values.get('callee_nbr', None)
        send_txt = request.values.get('send_txt', None)
    logger.debug('电话号码：{0}，告警信息：{1}'.format(callee_nbr, send_txt))
    # exit()
    if not send_txt:
        return json_msg(400, '语音消息字符串为空')
    elif send_txt.__len__() > 8:
        return json_msg(400, '传入的语音消息字符串长度不能大于8')
    if not callee_nbr:
        return json_msg(400, '电话号码为空')

    phone_nbr = '+86{0}'.format(callee_nbr)
    playInfoList = getPlayInfoList('2babeiamIPaddriamIPaddrafefd', [send_txt])
    ret = voiceNotifyAPI('+iamIPaddr', phone_nbr, playInfoList)
    # resultcode，只有 0 表示成功，其余均为失败，iamIPaddr 表示号码填写不合法
    if int(ret.get("resultcode", iamIPaddr)) == 0:
        return json_msg(200, '拨打电话成功')
    else:
        return json_msg(400, '拨打电话失败')