if __name__=="__main__":
    from prc import PRCClient

    # Starts PRCClient
    #
    # Only stderr is redirected to RPCClient output
    # To redirect stdout type following code in PRCClient console:
    #   import sys
    #   sys.stdout = __prcconsole__
    #
    # Type exit() for exit.
    PRCClient().start()
