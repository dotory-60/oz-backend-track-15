# mutable<생성 후에 변할 수 있다>, immutable<생성 후에 변할 수 있다.>

my_tuple: tuple[str, str] = ("str", "str") # tuple은 길이까지 지정해야 한다

# 길이를 모르는 경우에는 어떻게 할까?
my_tuple2: tuple[str, ...] = ("str", "str", "str", "str")

my_dict: dict[str, int] = {"a": 1, "b": 2, "c": 3}

or_type_list: list[str | int] = ["str", 12]

def add(a: int, b: int) -> None:
    return a + b

print(2 + add(1, 1))