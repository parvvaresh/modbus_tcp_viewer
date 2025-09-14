from modbus_utils import read_modbus_data

def test_modbus_connection():
    result = read_modbus_data(unit_id=1, host="127.0.0.1", port=1502)
    assert isinstance(result, dict)
    assert "coils" in result
    assert isinstance(result["coils"], list)
