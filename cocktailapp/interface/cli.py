import sys

from cocktailapp import constants


def get_app_args() -> str:
    cli_args = " ".join(sys.argv[1:])
    return cli_args


def parse_start_params(cli_args: str) -> tuple[str]:
    raw_arg_tokens = cli_args.split(",")
    stripped_arg_tokens = (rawtoken.strip().lower() for rawtoken in raw_arg_tokens)
    nonempty_stripped_tokens = filter(None, stripped_arg_tokens)
    result_tokens = tuple(nonempty_stripped_tokens)
    return result_tokens


def parse_args() -> dict:
    arg_dict = dict()

    raw_cli_args = get_app_args()
    parsed_args = parse_start_params(cli_args=raw_cli_args)

    arg_dict[constants.ARG_INGREDIENTS] = parsed_args
    return arg_dict


if __name__ == '__main__':
    print(parse_args())
