import serverlogger

def main():
    logger1 = serverlogger.ServerLogger.Instance()
    logger2 = serverlogger.ServerLogger.Instance()

    print(logger1)
    print(logger2)


if __name__ == "__main__":
    main()
