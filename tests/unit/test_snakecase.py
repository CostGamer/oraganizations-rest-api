import pytest

from app.core.utils import to_snake_case


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("CamelCase", "camel_case"),
        ("HTTPRequest", "http_request"),
        ("MyHTTPServer", "my_http_server"),
        ("simpleTest", "simple_test"),
        ("Test123Number", "test123_number"),
        ("JSONParser", "json_parser"),
        ("testCaseWithABCInside", "test_case_with_abc_inside"),
        ("snake_case", "snake_case"),
        ("already_snake_case", "already_snake_case"),
        ("Single", "single"),
        ("X", "x"),
        ("", ""),
        ("lowercase", "lowercase"),
        ("ALLUPPERCASE", "alluppercase"),
        ("Some4You", "some4_you"),
        ("A1B2C3", "a1_b2_c3"),
        ("PascalCaseTest", "pascal_case_test"),
        ("TestABCDataXYZ", "test_abc_data_xyz"),
    ],
)
def test_to_snake_case(input_str: str, expected: str) -> None:
    assert to_snake_case(input_str) == expected
