import csv
from django.shortcuts import render
from .models import Component
from .forms import BOMUploadForm


def home(request):
    return render(request, 'home.html')  # Replace 'home.html' with the template you want to render

def upload_bom(request):
    if request.method == "POST":
        form = BOMUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pcb_count = form.cleaned_data['pcb_count']
            file = request.FILES['file']

            # Parse CSV file
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            results = []
            min_pcbs_that_can_be_completed = pcb_count  # Start by assuming we can complete all PCBs
            all_pcbs_completed = True  # Flag to track if all PCBs are fully completed

            for row in reader:
                component_name = row['component_name']
                quantity_per_pcb = int(row['quantity'])
                required_quantity = quantity_per_pcb * pcb_count
                component = Component.objects.filter(name=component_name).first()

                if component:
                    # Check if available quantity is sufficient for the required quantity
                    is_sufficient = component.available_quantity >= required_quantity
                    remaining_quantity = component.available_quantity - required_quantity if is_sufficient else component.available_quantity
                    
                    # Calculate the maximum number of PCBs that can be completed for this component
                    pcbs_that_can_be_completed = component.available_quantity // quantity_per_pcb

                    # Ensure the number of PCBs that can be completed does not exceed the selected PCB count
                    pcbs_that_can_be_completed = min(pcbs_that_can_be_completed, pcb_count)

                    # Track the limiting factor, i.e., the component that can complete the fewest PCBs
                    min_pcbs_that_can_be_completed = min(min_pcbs_that_can_be_completed, pcbs_that_can_be_completed)

                    # If any component is insufficient, mark that not all PCBs can be completed
                    if not is_sufficient:
                        all_pcbs_completed = False

                    results.append({
                        'component_name': component_name,
                        'required_quantity': required_quantity,
                        'available_quantity': component.available_quantity,
                        'is_sufficient': is_sufficient,
                        'remaining_quantity': remaining_quantity,
                        'pcbs_that_can_be_completed': pcbs_that_can_be_completed
                    })

                    # Update component quantity if sufficient
                    if is_sufficient:
                        component.available_quantity = remaining_quantity
                        component.save()
                else:
                    results.append({
                        'component_name': component_name,
                        'required_quantity': required_quantity,
                        'available_quantity': 0,
                        'is_sufficient': False,
                        'remaining_quantity': 0,
                        'pcbs_that_can_be_completed': 0
                    })

            # Determine if all PCBs can be completed or the limiting factor
            if all_pcbs_completed:
                pcbs_status = f"All {pcb_count} PCBs can be fully completed."
            else:
                pcbs_status = f"Only {min_pcbs_that_can_be_completed} PCB(s) can be fully completed due to insufficient components."

            return render(request, 'bom_results.html', {
                'results': results,
                'pcbs_status': pcbs_status,
                'pcbs_completed': min_pcbs_that_can_be_completed
            })

    else:
        form = BOMUploadForm()

    return render(request, 'upload_bom.html', {'form': form})
