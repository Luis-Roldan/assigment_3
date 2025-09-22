from django.shortcuts import render
from django.http import HttpResponse

def math_form(request):
    """Display the form to input x, y, z values"""
    return render(request, 'math_operations/math_form.html')

def math_results(request):
    """Process the form data and perform math operations"""
    if request.method == 'POST':
        try:
            # Get values from form
            x = float(request.POST.get('x', 0))
            y = float(request.POST.get('y', 0))
            z = float(request.POST.get('z', 0))
            
            # Store original values
            original_x = x
            original_y = y
            original_z = z
            
            # Store intermediate results for display
            steps = []
            
            # Step 1: x += y
            x += y
            steps.append({
                'operation': f'{original_x} += {y}',
                'result': x,
                'description': 'x += y'
            })
            
            # Step 2: x -= z
            x -= z
            steps.append({
                'operation': f'{steps[0]["result"]} -= {z}',
                'result': x,
                'description': 'x -= z'
            })
            
            # Step 3: x *= y
            x *= y
            steps.append({
                'operation': f'{steps[1]["result"]} *= {y}',
                'result': x,
                'description': 'x *= y'
            })
            
            # Step 4: x %= z (if z ≠ 0)
            if z != 0:
                x %= z
                steps.append({
                    'operation': f'{steps[2]["result"]} %= {z}',
                    'result': x,
                    'description': 'x %= z'
                })
            else:
                steps.append({
                    'operation': 'Cannot perform modulo by zero',
                    'result': x,
                    'description': 'x %= z (skipped - division by zero)'
                })
            
            # Step 5: x /= z (if z ≠ 0)
            if z != 0:
                x /= z
                steps.append({
                    'operation': f'{steps[-1]["result"]} /= {z}',
                    'result': x,
                    'description': 'x /= z'
                })
            else:
                steps.append({
                    'operation': 'Cannot divide by zero',
                    'result': x,
                    'description': 'x /= z (skipped - division by zero)'
                })
            
            # Final result: x + y + z
            final_result = x + original_y + original_z
            
            context = {
                'original_x': original_x,
                'original_y': original_y,
                'original_z': original_z,
                'steps': steps,
                'final_x': x,
                'final_result': final_result,
                'success': True
            }
            
        except (ValueError, TypeError) as e:
            context = {
                'error': 'Please enter valid numbers for x, y, and z',
                'success': False
            }
        except Exception as e:
            context = {
                'error': f'An unexpected error occurred: {str(e)}',
                'success': False
            }
    else:
        # If not POST, redirect to form
        return render(request, 'math_operations/math_results.html')
    
    return render(request, 'math_operations/math_results.html', context)
