from src.manager import Manager
from src.models import Parameters
from src.models import Transfer

def test_total_due_pln():
    manager = Manager(Parameters())

    apartment_settlement = manager.get_settlement(
        'apart-polanka',
        2025,
        1
    )

    assert apartment_settlement is not None

    tenant_settlements = manager.create_tenants_settlements(
        apartment_settlement
    )

    assert isinstance(tenant_settlements, list)
    assert len(tenant_settlements) > 0

    tenants_total_due = sum(
        tenant.total_due_pln
        for tenant in tenant_settlements
    )

    apartment_costs = manager.get_apartment_costs(
        'apart-polanka',
        2025,
        1
    )

    assert tenants_total_due == apartment_settlement.total_due_pln
    assert tenants_total_due == apartment_costs

def test_get_tax_calculates_tax_on_tenant_income():
    manager = Manager(Parameters())

    manager.transfers = [
        Transfer(
            amount_pln=2500.0,
            date='2025-01-04',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-1'
        ),
        Transfer(
            amount_pln=2500.0,
            date='2025-01-05',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-2'
        ),
    ]

    tax = manager.get_tax(2025, 1, 0.085)

    assert tax == 425

def test_find_apartments_without_bills():
    manager = Manager(Parameters())

    manager.bills = [
        {
            "amount_pln": 760.00,
            "date_due": "2025-02-15",
            "settlement_year": 2025,
            "settlement_month": 1,
            "apartment": "apart-polanka",
            "type": "rent"
        }
    ]

    result = manager.find_apartments_without_bills(
        'apart-polanka',
        2025,
        1
    )

    assert result == []

    result = manager.find_apartments_without_bills(
        'apart-polanka',
        2026,
        1
    )

    assert result == ['apart-polanka']