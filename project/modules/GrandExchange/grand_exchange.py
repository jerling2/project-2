"""
    Title: The Grand Exchange and Component.
    Brief: The system architecture for this project is built using the mediator
           pattern. The mediator of the system is called the 'Grand Exchange'.
           The Grand Exchange's role is to mediate messages between 'Components'.
    Author: Joseph.
"""
# ------------------------------ Logging Config ------------------------------ #
import logging
logger = logging.getLogger("project")


# ------------------------------ Grand Exchange ------------------------------ #
class GrandExchange:
    """
        Brief: The Grand Exchange is a singleton object whose role is to serve
               as a mediator for all internal system messages. From this, the
               Grand Exchange effectively decouples components from needing to
               know about each other and increases the separation of concern.

        Note:  The Grand Exchange follows the singleton design pattern, allowing
               only one instance of the Grand Exchange to exist at any given time.
               When the Grand Exchange's constructor is called, it retrieves the
               existing instance. This allows components to easily connect to the
               correct Grand Exchange and simplifies the integration process.
    """
    channels = dict()

    # Singleton Pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def add_listener(cls, component: "Component", topic: str):
        """ Add the component to its requested channels, and create new channels when necessary. """
        assert isinstance(component, Component)
        if topic not in cls.channels:  # Channel DNE
            cls.channels[topic] = list()
            cls.channels[topic].append(component)
        else:
            cls.channels[topic].append(component)
        return None
    
    def remove_listener(cls, component: "Component", topic: str):
        """ Remove the component from its requested channel, and delete empty channels """
        assert isinstance(component, Component)
        if topic not in cls.channels:
            logger.warning(channel_dne_warning(topic))
        elif component not in cls.channels[topic]:
            logger.warning(component_not_found_warning(component, topic))
        elif len(cls.channels[topic]) > 1:
            cls.channels[topic].remove(component)
        else:
            del cls.channels[topic]
        return None

    def notify(cls, topic: str, message: object):
        """ Notify all components who are subscribed to the topic about the message. """
        if topic not in cls.channels:
            return None  # Channel DNE, so do nothing. 
        for subscriber in cls.channels[topic]:
            subscriber.notify(topic, message)
        return None 


# --------------------------------- Component -------------------------------- #
class Component:
    """
        Brief: The Component class provides the protocols for communicating with
               the Grand Exchange. When a Component instance is initialized, it
               establishes a connection to the Grand Exchange by invoking the 
               Grand Exchange constructor (see Grand Exchange's documentation).
               The Component class provides the necessary protocols to subscribe,
               unsubscribe, and publish to channels on the Grand Exchange. The
               Component class does not provide the notify method and leaves the
               implementation of the notify method to the concrete classes.
    """
    def __init__(self):
        self.mediator = GrandExchange()

    def subscribe(self, topic: str):
        """ Subscribe this component to channels on the Grand Exchange. """
        self.mediator.add_listener(self, topic)
        return None

    def unsubscribe(self, topic: str):
        """ Unsubscribe this component to channels on the Grand Exchange. """
        self.mediator.remove_listener(self, topic)
        return None

    def publish(self, topic: str, message: object):
        """ Publish a message on the Grand Exchange """
        self.mediator.notify(topic, message)
        return None

    def notify(self, topic: str, message: object):
        """ Do something when this component recieves a message. """
        raise NotImplementedError("The 'notify' method must be defined in concrete classes")


# --------------------------------- Warnings --------------------------------- #
def channel_dne_warning(topic): 
    warnMsg = "!!!!!!!\n"
    warnMsg +=  f"WARNING: Grand Exchange : remove_listener() : "
    warnMsg += f"channel `{topic}` dones not exist\n"
    warnMsg += "!!!!!!!"
    return warnMsg

def component_not_found_warning(component, topic):
    warnMsg = "!!!!!!!\n"
    warnMsg +=  f"WARNING: Grand Exchange : remove_listener() : \n"
    warnMsg += f"component `{component}`\nwas not found in topic `{topic}`\n"
    warnMsg += "!!!!!!!"
    return warnMsg