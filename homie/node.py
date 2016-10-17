#!/usr/bin/env python
import logging
from homie.helpers import isIdFormat
logger = logging.getLogger(__name__)


class HomieNodeProp(object):
    """docstring for HomieNodeProp"""

    def __init__(self, prop):
        super(HomieNodeProp, self).__init__()
        self._prop = None
        self.prop = prop
        self.handler = None

    def settable(self, handler):
        self.handler = handler

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, prop):
        if isIdFormat(prop):
            self._prop = prop
        else:
            logger.warning("'{}' has no valid ID-Format".format(prop))


class HomeNodeRange(HomieNodeProp):
    """docstring for HomeNodeRange"""

    def __init__(self, prop, lower, upper):
        super(HomeNodeRange, self).__init__(prop)
        self.lower = lower
        self.upper = upper


class HomieNode(object):
    """docstring for HomieNode"""

    def __init__(self, nodeId, nodeType):
        super(HomieNode, self).__init__()
        self.nodeId = nodeId
        self.nodeType = nodeType
        self.props = {}

    def advertise(self, prop):
        if prop not in self.props:
            homeNodeProp = HomieNodeProp(prop)
            if homeNodeProp:
                self.props[prop] = homeNodeProp
                return(homeNodeProp)
        else:
            logger.warning("Property '{}' already announced.".format(prop))

    def advertiseRange(self, prop, lower, upper):
        if prop not in self.props:
            homeNodeRange = HomeNodeRange(prop, lower, upper)
            if homeNodeRange:
                self.props[prop] = homeNodeRange
                return(homeNodeRange)
        else:
            logger.warning("Property '{}' already announced.".format(prop))

    def getProperties(self):
        data = ""
        for k, v in self.props.items():

            if data:    # join by comma
                data += "," + k
            else:       # nothing to join
                data = k

            if isinstance(v, HomeNodeRange):
                data += "[{}-{}]".format(
                    v.lower,
                    v.upper,
                )

            if v.handler:
                data += ":settable"

        return data

    @property
    def nodeId(self):
        return self._nodeId

    @nodeId.setter
    def nodeId(self, nodeId):
        self._nodeId = nodeId

    @property
    def nodeType(self):
        return self._nodeType

    @nodeType.setter
    def nodeType(self, nodeType):
        self._nodeType = nodeType


def main():
    pass


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")
