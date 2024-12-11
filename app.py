from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_base_name(base):
    return {
        2: 'binary',
        8: 'octal',
        10: 'decimal',
        16: 'hexadecimal'
    }[base]

def convert_number(number, from_base, to_base):
    try:
        # First convert to decimal with steps
        decimal, to_decimal_steps = convert_to_decimal(number, from_base)
        
        # Then convert from decimal to target base
        if to_base == 2:
            result = bin(decimal)[2:]
            conversion_steps = generate_steps(decimal, 2)
        elif to_base == 8:
            result = oct(decimal)[2:]
            conversion_steps = generate_steps(decimal, 8)
        elif to_base == 16:
            result = hex(decimal)[2:].upper()
            conversion_steps = generate_steps(decimal, 16)
        else:
            result = str(decimal)
            conversion_steps = "The number is already in decimal"

        # Combine all steps
        all_steps = []
        if from_base != 10:  # Only show decimal conversion if needed
            all_steps.append("Step 1: Convert to decimal first")
            all_steps.append(to_decimal_steps)
        
        if to_base != 10:  # Only show target base conversion if needed
            step_num = 2 if from_base != 10 else 1
            all_steps.append(f"\nStep {step_num}: Convert decimal to {get_base_name(to_base)}")
            all_steps.append(conversion_steps)

        return {
            'result': result,
            'steps': '\n'.join(all_steps),
            'formatted_result': format_result(result, to_base)
        }
    except ValueError:
        return {'error': 'Invalid input number for the selected base'}

def convert_to_decimal(number, from_base):
    if from_base == 10:
        return int(number), ""
    
    steps = []
    decimal = 0
    number = str(number).upper()
    
    # Dictionary for superscript numbers
    superscript = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    
    def get_superscript(n):
        return ''.join(superscript[d] for d in str(n))
    
    base_subscript = {
        2: '₂',
        8: '₈',
        10: '₁₀',
        16: '₁₆'
    }
    
    if from_base == 16:
        steps.append(f"Converting {number}₁₆ to decimal:")
        steps.append("Using place values:")
        digits = []
        for i, digit in enumerate(reversed(number)):
            value = int(digit, 16) if digit.isdigit() else (ord(digit) - ord('A') + 10)
            power = 16 ** i
            term = value * power
            digits.insert(0, f"{digit} × 16{get_superscript(i)} = {value} × {power} = {term}")
            decimal += term
        steps.extend(digits)
        steps.append(f"Sum all terms: {' + '.join(str(int(d.split('=')[-1])) for d in digits)}")
        steps.append(f"Decimal value = {decimal}₁₀")
    
    elif from_base in [2, 8]:
        base_name = "binary" if from_base == 2 else "octal"
        steps.append(f"Converting {number}{base_subscript[from_base]} to decimal:")
        steps.append("Using place values:")
        digits = []
        for i, digit in enumerate(reversed(number)):
            value = int(digit)
            power = from_base ** i
            term = value * power
            digits.insert(0, f"{digit} × {from_base}{get_superscript(i)} = {value} × {power} = {term}")
            decimal += term
        steps.extend(digits)
        steps.append(f"Sum all terms: {' + '.join(str(int(d.split('=')[-1])) for d in digits)}")
        steps.append(f"Decimal value = {decimal}₁₀")
    
    return decimal, '\n'.join(steps)

def generate_steps(decimal, base):
    if decimal == 0:
        return "0"
    
    steps = []
    quotient = decimal
    digits = []
    
    # Create division steps with HTML table
    steps.append("\nDivision method:")
    steps.append('<table class="conversion-table">')
    if base == 16:
        steps.append('<tr><th>Division</th><th>Quotient</th><th>Remainder</th><th>Hex</th></tr>')
    else:
        steps.append('<tr><th>Division</th><th>Quotient</th><th>Remainder</th></tr>')
    
    while quotient > 0:
        remainder = quotient % base
        if base == 16:
            if remainder > 9:
                hex_char = chr(ord('A') + remainder - 10)
            else:
                hex_char = str(remainder)  # For values 0-9, use the same number
            remainder_str = str(remainder)
            steps.append(f'<tr><td>{quotient} ÷ {base}</td><td>{quotient // base}</td><td>{remainder_str}</td><td>{hex_char}</td></tr>')
            digits.insert(0, hex_char)
        else:
            remainder_str = str(remainder)
            steps.append(f'<tr><td>{quotient} ÷ {base}</td><td>{quotient // base}</td><td>{remainder_str}</td></tr>')
            digits.insert(0, remainder_str)
        quotient //= base
    
    steps.append('</table>')
    result = ''.join(digits)
    
    # Add subscript to the final answer
    base_subscript = {
        2: '₂',
        8: '₈',
        10: '₁₀',
        16: '₁₆'
    }[base]
    
    steps.append(f"\nReading remainders from bottom to top:")
    steps.append(f"The {get_base_name(base)} number is: ({result}){base_subscript}")
    return '\n'.join(steps)

def format_result(result, base):
    base_subscript = {
        2: '₂',
        8: '₈',
        10: '₁₀',
        16: '₁₆'
    }
    return f"({result}){base_subscript[base]}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    number = data['number']
    from_base = int(data['from_base'])
    to_base = int(data['to_base'])
    
    return jsonify(convert_number(number, from_base, to_base))

if __name__ == '__main__':
    app.run(debug=True) 