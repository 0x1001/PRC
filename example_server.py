if __name__=="__main__":
    import time
    from prc import PRCServer

    PRCServer().start()

    while True:
        time.sleep(1)