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
from zope.session.interfaces import ISessionDataContainer
from zojax.layoutform import Fields, PageletEditForm


class ConfigureForm(PageletEditForm):

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
