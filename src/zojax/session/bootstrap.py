##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import transaction
from zope import component
from zope.app.appsetup.bootstrap import ensureUtility, getInformationFromEvent
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent

from zope.session.interfaces import IClientIdManager
from zope.session.http import CookieClientIdManager


@component.adapter(IDatabaseOpenedWithRootEvent)
def bootStrapSubscriber(event):
    db, connection, root, root_folder = getInformationFromEvent(event)

    ensureUtility(
        root_folder, IClientIdManager, 'CookieClientIdManager',
        CookieClientIdManager, asObject=True)

    transaction.commit()
    connection.close()
