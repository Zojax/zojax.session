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
from zope import interface, schema, i18nmessageid
from zope.session.http import ICookieClientIdManager

from zojax.widget.radio.field import RadioChoice


_ = i18nmessageid.MessageFactory('zojax.session')


class ISessionConfiglet(interface.Interface):
    """ session configlet """

    session = interface.Attribute('Session data container object')

    sessiontype = RadioChoice(
        title = u'Session type',
        description = u'Select session type.',
        vocabulary = "session.data.factory",
        required = True)


class ISessionDataFactory(interface.Interface):
    """ session factory """

    name = interface.Attribute('Plugin name')

    title = schema.TextLine(
        title = u'Title',
        required=True)

    description = schema.TextLine(
        title = u'Description',
        required=False)

    session = interface.Attribute("ISession object")

    def install():
        """ install plugin """

    def uninstall():
        """ uninstall plugin """

    def isInstalled():
        """ is session installed """

    def isAvailable():
        """ is session available """
