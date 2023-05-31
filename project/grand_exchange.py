""" 
    NOTE: this is only an example and will be removed after the 
          real grand exchange is implemented. 
"""

class Mediator:
    def __init__(self):
        self.channels = dict()
        
    def add_listener(self, component: "Component", topic: str):
        """ Add the component to its requested channels, and create new channels when necessary. """
        assert isinstance(component, Component)
        if topic not in self.channels:  # Channel DNE
            self.channels[topic] = list()
            self.channels[topic].append(component)
        else:
            self.channels[topic].append(component)
        return None

    def notify(self, topic: str, message: object):
        """ Notify all components who are subscribed to the topic about the message. """
        if topic not in self.channels:
            return None  # Channel DNE, so do nothing. 
        for subscriber in self.channels[topic]:
            subscriber.notify(topic, message)
        return None 


class Component:
    def __init__(self):
        self.mediator = None

    def connect(self, mediator: "Mediator"):
        """ Connect this component to a mediator. """
        assert isinstance(mediator, Mediator)
        self.mediator = mediator
        return None

    def subscribe(self, topic: str):
        """ Subscribe this component to channels on the mediator. """
        self.mediator.add_listener(self, topic)
        return None

    def publish(self, topic: str, message: object):
        """ Publish a message on the mediator """
        self.mediator.notify(topic, message)
        return None

    def notify(self, topic: str, message: object):
        """ Do something when this component recieves a message """
        raise NotImplementedError("The 'notify' method must be defined in concrete classes")


class Citizen(Component):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def notify(self, topic, message):
        print(f'{topic}: {message} {self.name} says "Well, ain\'t that mighty interestin.."')

    def eye_witness(self, message):
        self.publish("eye witness", message)
        return None


class NewsAnchor(Component):
    def __init__(self, organization):
        super().__init__()
        self.organization = organization

    def notify(self, topic, message):
        print(f'Here at the {self.organization}, this just in. {topic}: {message}')

    def breaking_news(self, message: str):
        self.publish("breaking news", message)
        return None


def main():
    # Create mediator and components.
    grand_exchange = Mediator()  # this will be a singleton!
    john_doe = Citizen("John Doe")
    us_news = NewsAnchor("US News")

    # Connect this component to the grand exchange.
    john_doe.connect(grand_exchange)
    us_news.connect(grand_exchange)
    
    # Subscribe to channels.
    john_doe.subscribe("breaking news")
    us_news.subscribe("eye witness")

    # Publish to channels.
    us_news.publish("breaking news", "Flordia declares independence!")
    john_doe.publish("eye witness", "Ah reckon I saw me a Florida Man ridin' an alligator.")

    #
    # Notice how the mediator relays the message! 
    #

    
if __name__ == "__main__":
    main()

