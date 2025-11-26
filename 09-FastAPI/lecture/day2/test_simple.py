from datetime import datetime, timedelta

# literal을 쓰지 않고 상수를 쓰는 이유
# 프로그램을 처음부터 개발한 개발자는 purchase_data + 2가 이틀 뒤 배송 도착이라는 것을 안다.
# 하지만, 새롭게 합류한 개발자라면 모를 수 있다. 따라서, 값에 이름표를 붙여주는 것이다.
# magic number
DELIVERY_DAYS = 2

def _is_holiday(day: datetime) -> bool:
    return day.weekday() > 5

def get_delivery_eta(purchase_date: datetime) -> datetime:
    current_date = purchase_date
    remaining_days = DELIVERY_DAYS

    while remaining_days > 0:
        current_date += timedelta(days=1)
        if not _is_holiday(current_date):
            remaining_days -= 1

    return current_date

def test_get_delivery_eta_2023_12_01() -> None:
    result = get_delivery_eta(datetime(2023, 12, 1))
    assert result == datetime(2023, 12, 4)

def test_get_delivery_eta_2024_12_31() -> None:
    """
    공휴일 정보가 없어서 1월 1일도 평일로 취급됩니다.
    """
    result = get_delivery_eta(datetime(2024, 12, 31))
    assert result == datetime(2025, 1, 2)

def test_get_delivery_eta_2024_02_28() -> None:
    result = get_delivery_eta(datetime(2024, 2, 28))
    assert result == datetime(2024, 3, 1)

def test_get_delivery_eta_2023_02_28() -> None:
    result = get_delivery_eta(datetime(2023, 2, 28))
    assert result == datetime(2023, 3, 2)





def add(a: int, b: int) -> int:
    return a + b

# 테스트 코드 (반대: 제품코드)
def test_add() -> None:
    # Given: 재료를 준비합니다
    # 버그는 "경계"를 좋아합니다
    a, b = 1, 1

    # When: 테스트 대상이되는 함수를 호출합니다
    result = add(a, b) # result의 타입은 int

    # Then:
    assert result == 2
