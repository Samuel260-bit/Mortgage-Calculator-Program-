"""
Author: Samuel Stewart
Date Written: 03/04/2025
Assignment: Final Project for a Mortgage Calculator
Short description: A program that calculates a monthly mortgage payment based on user inputs. The program also features an amortization schedule as well. 
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

def update_loan_amount(event=None):  # Event argument needed for binding
    try:
        home_price = float(home_price_entry.get()) if home_price_entry.get() else 0
        down_payment = float(down_payment_entry.get()) if down_payment_entry.get() else 0

        if down_payment > home_price:
            raise ValueError("Down payment cannot exceed home price.")

        loan_amount = home_price - down_payment
        loan_entry.config(state="normal")  # Allow updating the field
        loan_entry.delete(0, tk.END)
        loan_entry.insert(0, f"{loan_amount:.2f}")
        loan_entry.config(state="readonly")  # Set back to read-only
    except ValueError:
        loan_entry.config(state="normal")
        loan_entry.delete(0, tk.END)
        loan_entry.insert(0, "Error")
        loan_entry.config(state="readonly")

def get_float(entry):
    # Helper function to safely convert entry field input to float
    try:
        return float(entry.get()) if entry.get() else 0.0
    except ValueError:
        return None

def calculate_mortgage(): # Function to calculate the monthly mortgage payment based on the user inputs. it retrieves the values from the fields and applies te mortgage formula while updating the total monthly cost label
    try:
        loan_amount = get_float(loan_entry)
        if loan_amount is None or loan_amount <= 0:
            raise ValueError("Loan Amount must be a positive number.")

        interest_rate = get_float(interest_entry)
        if interest_rate is None or interest_rate < 0:
            raise ValueError("Interest Rate must be a non-negative number.")
        interest_rate = interest_rate / 100 / 12  # Convert annual % to monthly rate

        loan_term = term_entry.get()
        if not loan_term.isdigit() or int(loan_term) <= 0:
            raise ValueError("Loan Term must be a positive whole number.")
        loan_term = int(loan_term) * 12  # Convert years to months

        property_tax = get_float(property_tax_entry) / 12  # Convert yearly to monthly
        home_insurance = get_float(home_insurance_entry) / 12  # Convert yearly to monthly
        hoa_fees = get_float(hoa_fees_entry)
        pmi_percentage = get_float(pmi_entry) / 100  # Convert percentage to decimal
        pmi_cost = (loan_amount * pmi_percentage) / 12  # Convert yearly PMI to monthly

        # Mortgage Calculation
        monthly_payment = (loan_amount * interest_rate * (1 + interest_rate) ** loan_term) / \
                          ((1 + interest_rate) ** loan_term - 1)

        total_monthly_cost = monthly_payment + property_tax + home_insurance + hoa_fees + pmi_cost

        result_label.config(text=f"Total Monthly Payment: ${total_monthly_cost:.2f}")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


# Clear the fields 
def clear_fields():
    loan_entry.delete(0, tk.END)
    interest_entry.delete(0, tk.END)
    term_entry.delete(0, tk.END)
    property_tax_entry.delete(0, tk.END)
    home_insurance_entry.delete(0, tk.END)
    hoa_fees_entry.delete(0, tk.END)
    result_label.config(text="")
    pmi_entry.delete(0, tk.END)

# Amortization Schedule 
def open_amortization_window():
    amort_window = tk.Toplevel(root)
    amort_window.title("Amortization Schedule")
    amort_window.geometry("500x400")

    # Load and display the amortization schedule image
    try:
        schedule_icon = tk.PhotoImage(file="/Users/samuelstewart/Downloads/Mortgage Calculator Project/schedule_icon.png")
        schedule_label = tk.Label(amort_window, image=schedule_icon)
        schedule_label.pack()
        schedule_label.image = schedule_icon  # Keep reference to prevent garbage collection
    except Exception as e:
        schedule_label = tk.Label(amort_window, text="Amortization Schedule (Image Not Found)")
        schedule_label.pack()



    # Create a text widget to display amortization details
    text_area = tk.Text(amort_window, wrap="none", width=60, height=20)
    text_area.pack(padx=10, pady=10)

    # Display amortization schedule
    try:
        loan_amount = float(loan_entry.get())
        interest_rate = float(interest_entry.get()) / 100 / 12  # Convert to monthly rate
        loan_term = int(term_entry.get()) * 12  # Convert years to months

        if loan_term <= 0 or interest_rate < 0 or loan_amount <= 0:
            raise ValueError("Invalid input values")

        # Generate the amortization schedule
        balance = loan_amount
        monthly_payment = (loan_amount * interest_rate * (1 + interest_rate) ** loan_term) / \
                          ((1 + interest_rate) ** loan_term - 1)

        text_area.insert(tk.END, f"{'Month':<10}{'Principal':<15}{'Interest':<15}{'Balance':<15}\n")
        text_area.insert(tk.END, "-"*50 + "\n")

        for month in range(1, loan_term + 1):
            interest_payment = balance * interest_rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment

            text_area.insert(tk.END, f"{month:<10}{principal_payment:<15.2f}{interest_payment:<15.2f}{balance:<15.2f}\n")

        text_area.config(state="disabled")  # Make text read only

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

    # Close Button
    tk.Button(amort_window, text="Close", command=amort_window.destroy).pack(pady=5)


def exit_app():
    root.destroy()

# Create main application window
root = tk.Tk()
root.title("Mortgage Calculator")
root.geometry("400x300")

# Load and display the first image (Main Window - House Icon)
try:
    house_icon = tk.PhotoImage(file="/Users/samuelstewart/Downloads/Mortgage Calculator Project/house_icon.png")
    house_label = tk.Label(root, image=house_icon)
    house_label.pack()
    house_label.image = house_icon  # Keep reference to prevent garbage collection
except Exception as e:
    house_label = tk.Label(root, text="Mortgage Calculator (Image Not Found)")
    house_label.pack()

# Labels and Entry Fields
tk.Label(root, text="Home Price ($):").pack()
home_price_entry = tk.Entry(root)
home_price_entry.pack()
home_price_entry.bind("<KeyRelease>", update_loan_amount)  # Auto-update loan amount

tk.Label(root, text="Down Payment ($):").pack()
down_payment_entry = tk.Entry(root)
down_payment_entry.pack()
down_payment_entry.bind("<KeyRelease>", update_loan_amount)  # Auto-update loan amount

tk.Label(root, text="Loan Amount ($):").pack()
loan_entry = tk.Entry(root, state="readonly")  # Read-only since it's auto-calculated
loan_entry.pack()

tk.Label(root, text="Interest Rate (% per year):").pack()
interest_entry = tk.Entry(root)
interest_entry.pack()

tk.Label(root, text="Loan Term (Years):").pack()
term_entry = tk.Entry(root)
term_entry.pack()

tk.Label(root, text="Yearly Property Tax ($):").pack()
property_tax_entry = tk.Entry(root)
property_tax_entry.pack()

tk.Label(root, text="Yearly Home Insurance ($):").pack()
home_insurance_entry = tk.Entry(root)
home_insurance_entry.pack()

tk.Label(root, text="Monthly HOA Fees ($):").pack()
hoa_fees_entry = tk.Entry(root)
hoa_fees_entry.pack()

tk.Label(root, text="PMI (%):").pack()
pmi_entry = tk.Entry(root)
pmi_entry.pack()



# Buttons
tk.Button(root, text="Calculate", command=calculate_mortgage).pack()
tk.Button(root, text="Clear", command=clear_fields).pack()
tk.Button(root, text="Exit", command=exit_app).pack()
tk.Button(root, text="View Amortization Schedule", command=open_amortization_window).pack()

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack()

# Run the application
root.mainloop()
