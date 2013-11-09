if __name__=="__main__":
    from prc import PRCServer
    import time

    # Creates PRCServer object
    server = PRCServer()

    # Example of a mutable variable
    counter = [0]

    # This will allow access to counter variable in PRC
    server.add_variable("counter",counter)

    # Starts PRCServer. Non blocking!
    server.start()

    # Example of worker thread that increments counter
    while True:
        counter[0] += 1
        time.sleep(1)
