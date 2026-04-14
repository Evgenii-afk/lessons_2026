import pytest
import math 
from bounded_counter import BoundedCounter
from unittest.mock import patch, MagicMock

class TestBoundCounter:
    def setup_class(self):
        self.default_counter = BoundedCounter(0, 10, 5)

    def setup_method(self):
        self.counter = BoundedCounter(0, 10, 5)

    def test_ini_value(self):
        assert self.counter.get_value() == 5

    def test_incr(self):
        self.counter.increment(3)
        assert self.counter.get_value() == 8

    def test_decr(self):
        self.counter.decrement(2)
        assert self.counter.get_value() == 3

    def test_reset(self):
        self.counter.increment(4)
        self.counter.reset()
        assert self.counter.get_value() == 5


    @pytest.mark.parametrize('min_val, max_val, initial, expected', [
        (0, 10, None, 0),      
        (0, 10, 5, 5),         
        (0, 10, 0, 0),         
        (0, 10, 10, 10),       
        (-5, 5, 0, 0),         
        (0, 0, 0, 0),          
    ], ids=['default_initial', 'middle', 'lower_bound', 'upper_bound', 'negative_bounds', 'equal_bounds'])
    def test_creation_parametrized(self, min_val, max_val, initial, expected):
        if initial is None:
            counter = BoundedCounter(min_val, max_val)
        else:
            counter = BoundedCounter(min_val, max_val, initial)
        assert counter.get_value() == expected    


    @pytest.mark.parametrize('min_val, max_val, initial, exception_msg', [
        (10, 0, None, "min_value must be <= max_value"),
        (0, 10, -1, "initial_value out of bounds"),
        (0, 10, 11, "initial_value out of bounds"),
        (5, 5, 6, "initial_value out of bounds"),
    ], ids=['min_greater_than_max', 'initial_too_low', 'initial_too_high', 'initial_out_of_equal_bounds'])
    def test_creation_exceptions_parametrized(self, min_val, max_val, initial, exception_msg):
        """Параметризованный тест исключений при создании"""
        with pytest.raises(ValueError, match=exception_msg):
            BoundedCounter(min_val, max_val, initial)

        
    def test_increment_mocked(self, mock_increment):
        counter = BoundedCounter(0, 10, 5)
        counter.increment(3)
        mock_increment.assert_called_once()
        mock_increment.assert_called_once_with(3)
        assert counter.get_value() == 5

    def test_reset_monkeypatched(self, monkeypatch):
        counter = BoundedCounter(0, 10, 5)
        counter.increment(3)
        assert counter.get_value() == 8
        
        def fake_reset(self):
            self._current = 10
        
        monkeypatch.setattr(counter, 'reset', fake_reset.__get__(counter))

        counter.reset()
        
        assert counter.get_value() == 10

    def test_magicmock_simple(self):
        mock_counter = MagicMock()
        
        mock_counter.get_value.return_value = 42
        
        mock_sum_result = MagicMock()
        mock_sum_result.get_value.return_value = 100
        mock_counter.__add__.return_value = mock_sum_result
        
        value = mock_counter.get_value()  
        assert value == 42
        
        mock_counter.get_value.assert_called_once()
        
        other_counter = MagicMock()
        result = mock_counter + other_counter
        assert result.get_value() == 100
        
        mock_counter.__add__.assert_called_once_with(other_counter)