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
from zope.session.interfaces import ISessionDataContainer, IClientIdManager
from zope.session.http import ICookieClientIdManager
from zojax.layoutform import Fields, PageletEditForm
from zope import component

from interfaces import _

class ConfigureClientIdManagerForm(PageletEditForm):
    
    label = _(u'Client Id') 

    prefix = "config.session.clientid."
    fields = Fields(ICookieClientIdManager)

    def update(self):
        self.manager = component.getUtility(IClientIdManager)
        if self.manager is None:
            return

        super(ConfigureClientIdManagerForm, self).update()

    def getContent(self):
        return self.manager

    def isAvailable(self):
        return self.manager is not None


class ConfigureForm(PageletEditForm):

    label = _(u'Session data') 

    prefix = "config.session.data."
    fields = Fields(ISessionDataContainer)

    def update(self):
        self.session = self.context.session
        if self.session is None:
            return

        super(ConfigureForm, self).update()

    def getContent(self):
        return self.session

    def isAvailable(self):
        session = self.session
        return session is not None and ISessionDataContainer.providedBy(session)
