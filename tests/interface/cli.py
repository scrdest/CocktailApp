import pytest

from cocktailapp.interface import cli


@pytest.mark.parametrize(
    ("cli_input", "expected"), (
            ("", ()),
            ("a,b", ("a", "b")),
            ("a, b", ("a", "b")),
            ("A, b", ("A", "b")),
            ("A, B", ("A", "B")),
            ("a, B, cD", ("a", "B", "cD")),
            ("a, B, cD-EfG", ("a", "B", "cD-EfG")),
            ("1,2", ("1", "2")),
            ("1,2", ("1", "2")),
    )
)
def test_parse_start_params(cli_input, expected):
    result = cli.parse_start_params(cli_args=cli_input)
    assert result == expected