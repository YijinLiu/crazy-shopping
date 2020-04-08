import argparse

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Checkout your wholefood carts.")

    parser.add_argument("--selenium-driver", type=str, default="firefox", help="firefox/chrome")
    parser.add_argument("--headless", dest='headless', action='store_true')
    parser.add_argument("--no-headless", dest='headless', action='store_false')
    parser.set_defaults(headless=True)
    parser.add_argument("--private", dest='private', action='store_true')
    parser.add_argument("--no-private", dest='private', action='store_false')
    parser.set_defaults(private=True)
    parser.add_argument("--user-agent", type=str, default="", help="customized user agent")

    parser.add_argument("--short_timeout_secs", type=int, default=10)
    parser.add_argument("--long_timeout_secs", type=int, default=20)

    return parser
