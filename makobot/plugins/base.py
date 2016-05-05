class Plugin(object):
    @property
    def enabled(self):
        """
        REturns true if the plugin has been enabled or false if not.
        Typically this will check if the necessary environment variables are
        set.

        :returns: True if enabled, False if disabled
        :rtype: boolean
        """
        return False

    def activate(self):
        """
        Handles the activation of the plugin, typically this would be
        instantiating a client or something similar.
        """
        raise NotImplementedError('Plugin activate method not implemented')

    def extract(self, message):
        """
        Extracts the relevant values from a message for use when generating a
        report. Values are expected to be stored as an attribute of the Plugin
        class.
        """
        raise NotImplementedError('Plugin extract method not implemented')

    def report(self, message, active=True):
        """
        Reports any potential vulnerabilities via Slackbot. If active then the
        expected response is a reply, if not active (passive) then send only
        messages that meet a certain threshold to reduce noise.
        """
        self.retrieve()
        if not any(self.reports.values()) and active:
            message.reply('No reports for %s' %
                          ', '.join(self.reports.keys()))
        for subject, report in self.reports.items():
            if report:
                if active:
                    message.reply(self.format(subject, report))
                elif self.threshold_met(report):
                    message.send(self.format(subject, report))
        self.react(message)

    def retrieve(self):
        """
        Retrieves reports from the configured reporting service and populates
        the reports dict accordingly. This method should work in concert with
        the extract method.
        """
        raise NotImplementedError('Plugin retrieve method not implemented')

    def format(self, subject, report):
        """
        Formats a report in some easily and quickly consumed format. This is
        typically called via the plugin's report method.
        """
        raise NotImplementedError('Plugin format method not implemented')

    def threshold_met(self, report):
        """
        Determine if a threshold has been met for a report before sending a
        message to an entire channel. This method should return a boolean,
        where True is to send the message.

        :returns: True if threshold met, False if not
        :rtype: boolean
        """
        return False

    def react(self, message):
        """
        Reacts to a report with an an emoticon of some kind. Typically a
        weather-based icon representing the severity of the risk is the most
        clearly understood.
        """
        pass
