# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     views
   Description :
   Author :       wdh
   date：          2019/8/27
-------------------------------------------------
   Change Activity:
                   2019/8/27:
-------------------------------------------------
"""

from . import skdlis
from .transbyorderid import trans_skdlis_by_order_id
from .err import TjAssemResultsException, Success


def _build_htmls(htmls, e, order_id):
    if isinstance(e, TjAssemResultsException):
        htmls.append("""
              <b>
                <font color="red">
                   <h2>失败</h2>
                </font>
              </b><br>
              预约号:<b>{}</b><br>
              姓名:<b>{}</b><br>
              项目组id:<b>{}</b><br>
              项目组名:<b>{}</b><br>
              消息:<b>{}</b><br>
              <hr>
            """.format(e.order_id, e.username, e.assem_id, e.assem_name, repr(e).replace('\n', '<br>'))
                     )

    elif isinstance(e, Success):
        htmls.append("""
                  <b>
                  <font color="blue">
                     <h2>上传成功</h2>
                  </font>
                  </b><br>
                  预约号:<b>{}</b><br>
                  姓名:<b>{}</b><br>
                  项目组id:<b>{}</b><br>
                  项目组名:<b>{}</b><br>
                  消息:<b>{}</b><br>
                  <hr>       
             """.format(e.order_id, e.username, e.assem_id, e.assem_name, e.msg)
                     )
    else:
        htmls.append("""
              <b>
              <font color="red">
                   <h2>失败</h2>
                </font>
              </b><br>
              预约号:<b>{}</b><br>
              消息:<b>{}</b><br>
              <hr>
            """.format(order_id, repr(e))
                     )


@skdlis.route('/<order_id>')
def upload_by_order_id(order_id):
    htmls = []
    try:
        msgs = trans_skdlis_by_order_id(order_id, None)
        for msg in msgs:
            _build_htmls(htmls, msg, order_id)
    except Exception as e:
        _build_htmls(htmls, e, order_id)

    return '\n'.join(htmls)
