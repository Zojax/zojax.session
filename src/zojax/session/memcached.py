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
from rwproperty import getproperty, setproperty
from zope import interface, event, component
from zope.proxy import sameProxiedObjects
from zope.component import getUtility, queryUtility, getSiteManager
from zope.component.interfaces import IComponentLookup
from zope.lifecycleevent import ObjectCreatedEvent
from zope.session.interfaces import ISessionDataContainer
from lovely.session.memcached import MemCachedSessionDataContainer
from lovely.memcached.interfaces import IMemcachedClient
from zojax.memcached.interfaces import IMemcachedClientUnregisterEvent

from interfaces import ISessionDataFactory


class MemcachedSessionFactory(object):
    interface.implements(ISessionDataFactory)

    name = u'session.memcached'
    title = u'Memcached Session'
    description = u'A Session data container that stores data in Memcached.'

    @property
    def session(self):
        return getSiteManager().get(self.name)

    def install(self):
        if self.session is not None:
            raise ValueError(u'Session data container already installed.')

        sm = getSiteManager()

        container = MemCachedSessionDataContainer()
        event.notify(ObjectCreatedEvent(container))

        sm[self.name] = container

        sm.registerUtility(container, ISessionDataContainer)

    def uninstall(self):
        sm = getSiteManager()

        if self.name in sm:
            sm.unregisterUtility(sm[self.name], ISessionDataContainer)
            del sm[self.name]

    def isInstalled(self):
        container = queryUtility(ISessionDataContainer)
        if container is not None:
            if isinstance(container, MemCachedSessionDataContainer) and \
                    sameProxiedObjects(
                IComponentLookup(container), getSiteManager()):
                return True

        return False

    def isAvailable(self):
        return queryUtility(IMemcachedClient) is not None


@component.adapter(IMemcachedClientUnregisterEvent)
def memcachedClientUnregisterHandler(ev):
    factory = getUtility(ISessionDataFactory, 'memcached')
    if factory.isInstalled():
        factory.uninstall()

        factory = getUtility(ISessionDataFactory, 'ram')
        factory.install()
