import os


class NordVPN:

    terminal = None

    updateAvailable = False

    def __init__(self, Terminal=None):
        terminal = Terminal

    def ExecuteCommand(self, command):
        """
        Used Internally
        :param command:
        :return:
        """

        try:
            executeResponse = os.popen(command).read()
            self.terminal.appendPlainText(executeResponse)
            return self.FilterResponse(executeResponse)
        except Exception as e:
            print(e)
            return 0

    def Connect(self):
        """
        Connects to closest server
        :return:
        """

        return self.ExecuteCommand('nordvpn connect')

    def ConnectByCountry(self, country, city):
        """

        :param country:
        :param city:
        :return:
        """

        return self.ExecuteCommand('nordvpn connect {} {}'.format(country, city))

    def ConnectByServerCode(self, code):
        """

        :param country:
        :param city:
        :return:
        """

        return self.ExecuteCommand('nordvpn connect {}'.format(code))

    def Disconnect(self):
        """

        :return:
        """

        return self.ExecuteCommand('nordvpn disconnect')

    def LogOut(self):
        """

        :return:
        """

        return self.ExecuteCommand('nordvpn logout')

    def GetStatus(self):
        """

        :return:
        """

        return self.ExecuteCommand('nordvpn status')

    def GetAccount(self):
        """

        :return:
        """

        return self.ExecuteCommand('nordvpn account')

    def GetCountries(self):
        return self.ExecuteCommand('nordvpn countries')

    def GetCities(self, country):
        return self.ExecuteCommand('nordvpn cities {}'.format(country))

    def FilterResponse(self, message):
        """
        Filter out text information from data received from terminal after command execution
        :param response:
        :return:
        """

        lines = message.split('\n')

        response = ''
        for line in lines:
            s = line.strip()

            if s not in ['\\', '-', '/', '|', '', '\n'] and ('Please update' not in s):
                response = response + s + '\n'
            if 'Please update' in s:
                self.updateAvailable = True

        return response
