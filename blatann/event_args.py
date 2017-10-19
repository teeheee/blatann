

class EventArgs(object):
    pass

# Gap Event Args


class DisconnectionEventArgs(EventArgs):
    def __init__(self, reason):
        self.reason = reason


# SMP Event Args

class AuthenticationStatusEventArgs(EventArgs):
    def __init__(self, status):
        self.status = status


class PasskeyEntryEventArgs(EventArgs):
    def __init__(self, key_type, resolve):
        self.key_type = key_type
        self.resolve = resolve


class PasskeyDisplayEventArgs(EventArgs):
    def __init__(self, passkey, match_request):
        self.passkey = passkey
        self.match_request = match_request


# Gatt Server Event Args

class WriteEventArgs(EventArgs):
    def __init__(self, value):
        self.value = value


class SubscriptionStateChangeEventArgs(EventArgs):
    def __init__(self, subscription_state):
        """
        :type subscription_state: blatann.gatt.SubscriptionState
        """
        self.subscription_state = subscription_state


# Gatt Client Event Args

class ReadCompleteEventArgs(EventArgs):
    def __init__(self, value, status):
        self.value = value
        self.status = status


class WriteCompleteEventArgs(EventArgs):
    def __init__(self, value, status):
        self.value = value
        self.status = status


class SubscriptionWriteCompleteEventArgs(EventArgs):
    def __init__(self, value, status):
        self.value = value
        self.status = status


class NotificationReceivedEventArgs(EventArgs):
    def __init__(self, value, is_indication):
        self.value = value
        self.is_indication = is_indication


class DatabaseDiscoveryCompleteEventArgs(EventArgs):
    def __init__(self, status):
        self.status = status