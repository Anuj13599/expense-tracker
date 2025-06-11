from .models import CurrentBalance, TrackingHistory
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)

        # Handle empty or invalid amount input
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid amount.")
            return redirect('/')

        if amount == 0:
            messages.error(request, "Amount cannot be zero.")
            return redirect('/')

        expense_type = "CREDIT" if amount > 0 else "DEBIT"

        # Create tracking history
        tracking_history = TrackingHistory.objects.create(
            amount=amount,
            expense_type=expense_type,
            current_balance=current_balance,
            description=description
        )

        # Update balance
        current_balance.current_balance += amount
        current_balance.save()

        return redirect('/')

    # GET request handling
    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    income = 0
    expense = 0

    for tracking_history in TrackingHistory.objects.all():
        if tracking_history.expense_type == "CREDIT":
            income += tracking_history.amount
        else:
            expense += tracking_history.amount

    context = {
        'income': income,
        'expense': expense,
        'transactions': TrackingHistory.objects.all(),
        'current_balance': current_balance
    }

    return render(request, 'index.html', context)



def delete_transaction(request, id):
    tracking_history = TrackingHistory.objects.filter(id = id)

    if tracking_history.exists():
        current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
        tracking_history = tracking_history[0]
        
        current_balance.current_balance = current_balance.current_balance - tracking_history.amount

        current_balance.save()


    tracking_history.delete()
    return redirect('/')
