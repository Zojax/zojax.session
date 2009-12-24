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
from zope.component import getUtilitiesFor
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import ISessionDataFactory


def SessionFactories(context):

    terms = []
    for name, factory in getUtilitiesFor(ISessionDataFactory):
        if not factory.isAvailable():
            continue
        term = SimpleTerm(name, name, factory.title)
        term.description = factory.description
        terms.append((factory.title, name, term))

    terms.sort()
    return SimpleVocabulary([term for _t, _n, term in terms])
