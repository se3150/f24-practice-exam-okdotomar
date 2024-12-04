import pytest
from battery import Battery
from unittest.mock import Mock

todo = pytest.mark.skip(reason='todo: pending spec')

@pytest.fixture
def charged_battery():
    return Battery(100)

@pytest.fixture
def partially_charged_battery():
    b = Battery(100)
    b.mCharge = 70
    return b


def describe_Battery():

    def describe_recharge():
        # your test cases here
        def it_recharges_battery_50_percent(partially_charged_battery):
            assert partially_charged_battery.recharge(50) is True
            assert partially_charged_battery.getCharge() == 100

        def it_recharges_battery_90_percent(partially_charged_battery):
            assert partially_charged_battery.recharge(90) is True
            assert partially_charged_battery.getCharge() == 100

        def it_recharges_battery_more_than_100_percent(partially_charged_battery):
            assert partially_charged_battery.recharge(110) is True
            assert partially_charged_battery.getCharge() == 100

        def it_tries_to_recharge_a_negative_amount(partially_charged_battery):
            assert partially_charged_battery.recharge(-10) is False

        def it_connects_external_monitor_with_partially_charged_battery(partially_charged_battery):

            partially_charged_battery.external_monitor = Mock()
            partially_charged_battery.recharge(10)
            partially_charged_battery.external_monitor.notify_recharge.assert_called_once_with(80)

        def it_connects_external_monitor_with_charged_battery(charged_battery):
            charged_battery.external_monitor = Mock()
            charged_battery.drain(10)
            charged_battery.recharge(10)
            charged_battery.external_monitor.notify_recharge.assert_called_once_with(100)
        

    def describe_drain():
        # your test cases here
        def it_drains_battery_50_percent(charged_battery):
            assert charged_battery.drain(50) is True
            assert charged_battery.getCharge() == 50

        def it_drains_battery_90_percent(charged_battery):
            assert charged_battery.drain(90) is True
            assert charged_battery.getCharge() == 10

        def it_drains_battery_less_than_0_then_is_set_to_0(partially_charged_battery):
            assert partially_charged_battery.drain(100) is True
            assert partially_charged_battery.getCharge() == 0

        def it_tries_to_drain_a_negative_amount(charged_battery):
            assert charged_battery.drain(-10) is False
            assert charged_battery.getCharge() == 100

        def it_connects_external_monitor_with_partially_charged_battery(partially_charged_battery):
            external_monitor = Mock()
            partially_charged_battery.external_monitor = external_monitor
            partially_charged_battery.drain(10)
            partially_charged_battery.external_monitor.notify_drain.assert_called_once_with(60)

        def it_connects_external_monitor_with_charged_battery(charged_battery):
            external_monitor = Mock()
            charged_battery.external_monitor = external_monitor
            charged_battery.drain(10)
            charged_battery.external_monitor.notify_drain.assert_called_once_with(90)



