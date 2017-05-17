# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from twilio.base.domain import Domain
from twilio.rest.preview.sync import Sync
from twilio.rest.preview.wireless import Wireless


class Preview(Domain):

    def __init__(self, twilio):
        """
        Initialize the Preview Domain
        
        :returns: Domain for Preview
        :rtype: Preview
        """
        super(Preview, self).__init__(twilio)
        
        self.base_url = 'https://preview.twilio.com'
        
        # Versions
        self._wireless = None
        self._sync = None

    @property
    def wireless(self):
        """
        :returns: Version wireless of preview
        :rtype: Wireless
        """
        if self._wireless is None:
            self._wireless = Wireless(self)
        return self._wireless

    @property
    def sync(self):
        """
        :returns: Version sync of preview
        :rtype: Sync
        """
        if self._sync is None:
            self._sync = Sync(self)
        return self._sync

    @property
    def commands(self):
        """
        :rtype: CommandList
        """
        return self.wireless.commands

    @property
    def devices(self):
        """
        :rtype: DeviceList
        """
        return self.wireless.devices

    @property
    def rate_plans(self):
        """
        :rtype: RatePlanList
        """
        return self.wireless.rate_plans

    @property
    def services(self):
        """
        :rtype: ServiceList
        """
        return self.sync.services

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview>'