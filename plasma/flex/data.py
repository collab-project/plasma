# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Data Management Service implementation.

This module contains the message classes used with Flex Data Management
Service.
"""

import pyamf

from plasma.flex.messaging import messages

__all__ = [
    'DataMessage',
    'SequencedMessage',
    'PagedMessage',
    'DataErrorMessage'
]


class DataMessage(messages.AsyncMessage):
    """
    I am used to transport an operation that occured on a managed object
    or collection.

    This class of message is transmitted between clients subscribed to a
    remote destination as well as between server nodes within a cluster.
    The payload of this message describes all of the relevant details of
    the operation. This information is used to replicate updates and detect
    conflicts.

    @see: U{DataMessage on Livedocs (external)
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/DataMessage.html>}
    @ivar identity: Provides access to the identity map which defines the
        unique identity of the item affected by this DataMessage (relevant for
        create/update/delete but not fill operations).
    @ivar operation: Provides access to the operation/command of this
        DataMessage. Operations indicate how the remote destination should
        process this message.
    """

    def __init__(self, **kwargs):
        AsyncMessage.__init__(self, **kwargs)

        self.identity = kwargs.pop('identity', None)
        self.operation = kwargs.pop('operation', None)


class SequencedMessage(messages.AcknowledgeMessage):
    """
    Response to L{DataMessage} requests.

    @see: U{SequencedMessage on Livedocs (external)
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/SequencedMessage.html>}
    """

    def __init__(self, **kwargs):
        AcknowledgeMessage.__init__(self, **kwargs)
        #: Provides access to the sequence id for this message.
        #:
        #: The sequence id is a unique identifier for a sequence
        #: within a remote destination. This value is only unique for
        #: the endpoint and destination contacted.
        self.sequenceId = None
        #:
        self.sequenceProxies = None
        #: Provides access to the sequence size for this message.
        #:
        #: The sequence size indicates how many items reside in the
        #: remote sequence.
        self.sequenceSize = None
        #:
        self.dataMessage = None


class PagedMessage(SequencedMessage):
    """
    This messsage provides information about a partial sequence result.

    @see: U{PagedMessage on Livedocs (external)
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/PagedMessage.html>}
    """

    def __init__(self):
        SequencedMessage.__init__(self)
        #: Provides access to the number of total pages in a sequence
        #: based on the current page size.
        self.pageCount = None
        #: Provides access to the index of the current page in a sequence.
        self.pageIndex = None


class DataErrorMessage(messages.ErrorMessage):
    """
    Special cases of ErrorMessage will be sent when a data conflict
    occurs.

    This message provides the conflict information in addition to
    the L{ErrorMessage<pyamf.flex.messaging.ErrorMessage>} information.

    @see: U{DataErrorMessage on Livedocs (external)
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/DataErrorMessage.html>}
    """

    def __init__(self):
        ErrorMessage.__init__(self)
        #: The client oringinated message which caused the conflict.
        self.cause = None
        #: An array of properties that were found to be conflicting
        #: between the client and server objects.
        self.propertyNames = None
        #: The value that the server had for the object with the
        #: conflicting properties.
        self.serverObject = None


pyamf.register_package(globals(), package='flex.data.messages')
