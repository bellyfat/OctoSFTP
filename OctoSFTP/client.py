
import logging
import subprocess
from threading import Lock, Thread


class ClientList:
    """Stores client list and support functions for testing clients online"""

    def __init__(self, settings, client_file='clients.ini'):
        """Initialises the class"""
        # Logging
        self._logger = logging.getLogger(__name__)

        # Client arrays
        self.client_list = []

        self.clients_online = []
        self.clients_offline = []

        self.settings = settings
        self.client_file = client_file

        # Threading lock
        self.lock = Lock()

        # Begins populating class lists
        self.load_client_file()
        self.online_clients()

    def __str__(self):
        """Returns count of offline and online clients"""
        return "{0} online clients. {1} offline clients.".format(
            len(self.clients_online), len(self.clients_offline))

    def __iter__(self):
        """
        :return: iteration for online clients
        """
        return self.clients_online.__iter__()

    def __len__(self):
        """
        :return: len of clients online
        """
        return self.clients_online.__len__()

    def load_client_file(self):
        """
        Loads the clients from file
        """
        client_file = open(self.client_file, "r")

        with client_file:
            self.client_list = [client.strip() for client in client_file
                                if client.find("#") < 0 and client != "\n"]

        self.client_list.sort(reverse=True)

    def online_client_test(self, client):
        """
        Pings the client to test if online

        :param client: Client to test if online
        :return: Tuple of client name and online status: (client, Bool)
        """
        online = subprocess.call("ping -n " +
                                 self.settings.client_attempts +
                                 " " +
                                 client,
                                 stdout=subprocess.PIPE
                                 )

        if online == 0:
            self._logger.log(logging.INFO, "Client online: " + client)
            self.clients_online.append(client)
        else:
            self._logger.log(logging.WARNING, "Client offline: " + client)
            self.clients_offline.append(client)

    def thread_dequeue(self):
        """
        Threadsafe queue support function to prevent conflicts
        """
        while len(self.client_list) > 0:
            self.lock.acquire()
            client = self.client_list.pop()
            self.lock.release()

            # Pass popped client to function
            self.online_client_test(client)

    def online_clients(self):
        """
        Tests if all clients in client_list are online
        """
        active_threads = []

        # Spawn instances for multithreading
        for i in range(self.settings.client_threads):
            instance = Thread(target=self.thread_dequeue)
            active_threads.append(instance)
            instance.start()

        # Allow threads to complete before proceeding
        for instance in active_threads:
            instance.join()

        self.clients_online.sort()
        self.clients_offline.sort()
        self._logger.log(logging.INFO, "Clients online: " +
                         str(len(self.clients_online)))
        self._logger.log(logging.WARNING, "Clients offline: " +
                         str(len(self.clients_offline)))

        # TODO: Add logging for successful list creation
        # TODO: create logging for offline cases
