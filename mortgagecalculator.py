"""
Author: Samuel Stewart
Date Written: 02/18/2025
Assignment: Final project rough draft 
Short description: A program that calculates a monthly mortgag payment based on user inputs such as loan amount. interest rate, and loan term in years
"""
import tkinter as tk
from tkinter import messagebox

def calculate_mortgage():
    try:
        loan_amount = float(loan_entry.get())
        interest_rate = float(interest_entry.get()) / 100 / 12  # Convert to monthly rate
        loan_term = int(term_entry.get()) * 12  # Convert years to months
        
        if loan_term <= 0 or interest_rate < 0 or loan_amount <= 0:
            raise ValueError("Invalid input values")
        
        monthly_payment = (loan_amount * interest_rate * (1 + interest_rate) ** loan_term) / \
                          ((1 + interest_rate) ** loan_term - 1)
        
        result_label.config(text=f"Monthly Payment: ${monthly_payment:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

def clear_fields():
    loan_entry.delete(0, tk.END)
    interest_entry.delete(0, tk.END)
    term_entry.delete(0, tk.END)
    result_label.config(text="")

def exit_app():
    root.destroy()

# Create main application window
root = tk.Tk()
root.title("Mortgage Calculator")
root.geometry("400x300")

# Labels and Entry Fields
tk.Label(root, text="Loan Amount ($):").pack()
loan_entry = tk.Entry(root)
loan_entry.pack()

tk.Label(root, text="Interest Rate (% per year):").pack()
interest_entry = tk.Entry(root)
interest_entry.pack()

tk.Label(root, text="Loan Term (Years):").pack()
term_entry = tk.Entry(root)
term_entry.pack()

# Buttons
tk.Button(root, text="Calculate", command=calculate_mortgage).pack()
tk.Button(root, text="Clear", command=clear_fields).pack()
tk.Button(root, text="Exit", command=exit_app).pack()

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack()

# Run the application
root.mainloop()
