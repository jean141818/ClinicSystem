from datetime import datetime, date, time
import json
from typing import List, Dict, Optional

class Person:
    def __init__(self, id: str, name: str, last_name: str, email: str, phone: str):
        self._id = id
        self._name = name
        self._last_name = last_name
        self._email = email
        self._phone = phone
    
    def get_complete_info(self) -> str:
        raise NotImplementedError("Abstract method")
    
    def get_id(self) -> str:
        return self._id
    
    def get_full_name(self) -> str:
        return f"{self._name} {self._last_name}"
    
    def get_email(self) -> str:
        return self._email
    
    def __str__(self) -> str:
        return self.get_complete_info()

class Patient(Person):
    def __init__(self, id: str, name: str, last_name: str, email: str, phone: str, birth_date: date):
        super().__init__(id, name, last_name, email, phone)
        self._birth_date = birth_date
        self._medical_history = ConsultationList()
    
    def get_complete_info(self) -> str:
        age = self._calculate_age()
        return f"Patient: {self.get_full_name()} | ID: {self._id} | Age: {age} years"
    
    def _calculate_age(self) -> int:
        today = date.today()
        return today.year - self._birth_date.year - (
            (today.month, today.day) < (self._birth_date.month, self._birth_date.day))
    
    def add_consultation(self, consultation: 'Consultation') -> None:
        self._medical_history.add_consultation(consultation)
    
    def get_complete_history(self) -> List['Consultation']:
        return self._medical_history.get_all_consultations()
    
    def show_history(self) -> None:
        print(f"\n--- Medical History of {self.get_full_name()} ---")
        self._medical_history.show_history_recursive()

class Doctor(Person):
    def __init__(self, id: str, name: str, last_name: str, email: str, phone: str, specialty: str, consultation_fee: float):
        super().__init__(id, name, last_name, email, phone)
        self._specialty = specialty
        self._consultation_fee = consultation_fee
        self._schedule = AppointmentList()
    
    def get_complete_info(self) -> str:
        return f"Dr. {self.get_full_name()} | {self._specialty} | Fee: S/.{self._consultation_fee}"
    
    def schedule_appointment(self, appointment: 'Appointment') -> bool:
        return self._schedule.add_appointment(appointment)
    
    def get_daily_appointments(self, date: date) -> List['Appointment']:
        return self._schedule.get_appointments_by_date(date)
    
    def calculate_payment(self, start_date: date, end_date: date) -> float:
        simulated_consultations = [
            SimulatedConsultation(150.0),
            SimulatedConsultation(150.0),
            SimulatedConsultation(150.0)
        ]
        return self._calculate_total_recursive(simulated_consultations, 0)
    
    def _calculate_total_recursive(self, consultations: List['SimulatedConsultation'], index: int) -> float:
        if index >= len(consultations):
            return 0.0
        return consultations[index].fee + self._calculate_total_recursive(consultations, index + 1)

class Secretary(Person):
    def __init__(self, id: str, name: str, last_name: str, email: str, phone: str, shift: str, assigned_area: str):
        super().__init__(id, name, last_name, email, phone)
        self._shift = shift
        self._assigned_area = assigned_area
    
    def get_complete_info(self) -> str:
        return f"Secretary: {self.get_full_name()} | Shift: {self._shift} | Area: {self._assigned_area}"
    
    def register_patient(self, clinic: 'Clinic', patient: Patient) -> bool:
        return clinic.register_patient(patient)
    
    def schedule_medical_appointment(self, doctor: Doctor, patient: Patient, date: date, time: time, consultation_type: str) -> Optional['Appointment']:
        if doctor._schedule.check_availability(doctor, date, time):
            appointment = Appointment(
                f"C{datetime.now().strftime('%Y%m%d%H%M%S')}",
                date, time, doctor, patient, consultation_type
            )
            if doctor.schedule_appointment(appointment):
                return appointment
        return None

class ConsultationNode:
    def __init__(self, consultation: 'Consultation'):
        self.consultation = consultation
        self.next = None

class ConsultationList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def add_consultation(self, consultation: 'Consultation') -> None:
        new_node = ConsultationNode(consultation)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1
        print(f"✓ Consultation added to history. Total: {self.size} consultations")
    
    def find_consultation_by_date(self, date: date) -> Optional['Consultation']:
        current = self.head
        while current is not None:
            if current.consultation.get_date() == date:
                return current.consultation
            current = current.next
        return None
    
    def get_all_consultations(self) -> List['Consultation']:
        consultations = []
        current = self.head
        while current is not None:
            consultations.append(current.consultation)
            current = current.next
        return consultations
    
    def show_history_recursive(self, current_node=None) -> None:
        if current_node is None:
            current_node = self.head
            if current_node is None:
                print("No consultations registered")
                return
        
        if current_node is None:
            return
        
        consultation = current_node.consultation
        print(f"Date: {consultation.get_date()} | Doctor: {consultation.get_doctor().get_full_name()}")
        print(f"Diagnosis: {consultation.get_diagnosis()}")
        print("-" * 50)
        
        self.show_history_recursive(current_node.next)

class AppointmentNode:
    def __init__(self, appointment: 'Appointment'):
        self.appointment = appointment
        self.next = None

class AppointmentList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def add_appointment(self, appointment: 'Appointment') -> bool:
        new_node = AppointmentNode(appointment)
        
        if self.head is None or appointment.get_date_time() < self.head.appointment.get_date_time():
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            print(f"✓ Appointment scheduled successfully. Total appointments: {self.size}")
            return True
        
        current = self.head
        while current.next is not None and current.next.appointment.get_date_time() < appointment.get_date_time():
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        print(f"✓ Appointment scheduled successfully. Total appointments: {self.size}")
        return True
    
    def check_availability(self, doctor: Doctor, date: date, time: time) -> bool:
        date_time = datetime.combine(date, time)
        current = self.head
        
        while current is not None:
            if current.appointment.get_date_time() == date_time:
                return False
            current = current.next
        
        return True
    
    def find_appointment_by_patient(self, patient_id: str) -> List['Appointment']:
        found_appointments = []
        current = self.head
        
        while current is not None:
            if current.appointment.get_patient().get_id() == patient_id:
                found_appointments.append(current.appointment)
            current = current.next
        
        return found_appointments
    
    def get_appointments_by_date(self, date: date) -> List['Appointment']:
        date_appointments = []
        current = self.head
        
        while current is not None:
            if current.appointment.get_date() == date:
                date_appointments.append(current.appointment)
            current = current.next
        
        return date_appointments

class SimulatedConsultation:
    def __init__(self, fee: float):
        self.fee = fee

class Consultation:
    def __init__(self, consultation_id: str, date: date, time: time, doctor: Doctor, patient: Patient):
        self._consultation_id = consultation_id
        self._date = date
        self._time = time
        self._doctor = doctor
        self._patient = patient
        self._diagnosis = "General consultation"
        self._treatment = "Under observation"
        self._applied_fee = doctor._consultation_fee
    
    def get_date(self) -> date:
        return self._date
    
    def get_doctor(self) -> Doctor:
        return self._doctor
    
    def get_diagnosis(self) -> str:
        return self._diagnosis
    
    def register_diagnosis(self, diagnosis: str) -> None:
        self._diagnosis = diagnosis
    
    def register_treatment(self, treatment: str) -> None:
        self._treatment = treatment
    
    def calculate_fee(self) -> float:
        return self._applied_fee

class Appointment:
    def __init__(self, appointment_id: str, date: date, time: time, doctor: Doctor, patient: Patient, consultation_type: str):
        self._appointment_id = appointment_id
        self._date = date
        self._time = time
        self._doctor = doctor
        self._patient = patient
        self._consultation_type = consultation_type
        self._status = "Scheduled"
    
    def get_date(self) -> date:
        return self._date
    
    def get_date_time(self) -> datetime:
        return datetime.combine(self._date, self._time)
    
    def get_patient(self) -> Patient:
        return self._patient
    
    def confirm(self) -> None:
        self._status = "Confirmed"
    
    def cancel(self) -> None:
        self._status = "Cancelled"
    
    def get_appointment_info(self) -> str:
        return (f"Appointment {self._appointment_id} | {self._date} {self._time.strftime('%H:%M')} | "
                f"Patient: {self._patient.get_full_name()} | "
                f"Doctor: {self._doctor.get_full_name()} | Status: {self._status}")

class ConsultingRoom:
    def __init__(self, number: int, specialty: str):
        self._number = number
        self._specialty = specialty
        self._equipment = []
        self._available = True
        self._reservations = []
    
    def reserve(self, doctor: Doctor, date: date, time: time) -> bool:
        if self._available and self._specialty == doctor._specialty:
            self._available = False
            self._reservations.append((doctor, date, time))
            return True
        return False
    
    def release(self) -> None:
        self._available = True
    
    def check_availability(self, date: date, time: time) -> bool:
        for reservation in self._reservations:
            if reservation[1] == date and reservation[2] == time:
                return False
        return self._available

class Clinic:
    def __init__(self, name: str, address: str):
        self._name = name
        self._address = address
        self._patients = []
        self._doctors = []
        self._secretaries = []
        self._consulting_rooms = []
        self._patients_sorted = False
    
    def register_patient(self, patient: Patient) -> bool:
        for p in self._patients:
            if p.get_id() == patient.get_id():
                return False
        
        self._patients.append(patient)
        self._patients_sorted = False
        print(f"✓ Patient {patient.get_full_name()} registered successfully")
        return True
    
    def _sort_patients(self) -> None:
        if not self._patients_sorted:
            self._patients.sort(key=lambda p: p.get_id())
            self._patients_sorted = True
    
    def find_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        if not self._patients:
            return None
        
        self._sort_patients()
        
        left = 0
        right = len(self._patients) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_patient = self._patients[mid]
            
            if mid_patient.get_id() == patient_id:
                return mid_patient
            elif mid_patient.get_id() < patient_id:
                left = mid + 1
            else:
                right = mid - 1
        
        return None
    
    def find_patient_by_name(self, name: str) -> List[Patient]:
        results = []
        name_lower = name.lower()
        
        for patient in self._patients:
            if name_lower in patient.get_full_name().lower():
                results.append(patient)
        
        return results
    
    def hire_doctor(self, doctor: Doctor) -> bool:
        self._doctors.append(doctor)
        print(f"✓ Dr. {doctor.get_full_name()} hired successfully")
        return True
    
    def add_consulting_room(self, consulting_room: ConsultingRoom) -> None:
        self._consulting_rooms.append(consulting_room)
        print(f"✓ Consulting room {consulting_room._number} ({consulting_room._specialty}) added")
    
    def generate_payment_reports(self, start_date: date, end_date: date) -> Dict:
        reports = {}
        
        for doctor in self._doctors:
            payment = doctor.calculate_payment(start_date, end_date)
            reports[doctor.get_id()] = {
                'doctor': doctor.get_full_name(),
                'specialty': doctor._specialty,
                'payment': payment,
                'period': f"{start_date} to {end_date}"
            }
        
        return reports
    
    def get_operational_metrics(self) -> Dict:
        return {
            'total_patients': len(self._patients),
            'total_doctors': len(self._doctors),
            'total_secretaries': len(self._secretaries),
            'total_consulting_rooms': len(self._consulting_rooms),
            'specialties': list(set([doctor._specialty for doctor in self._doctors]))
        }
    
    def show_all_patients(self) -> None:
        print(f"\n--- REGISTERED PATIENTS ({len(self._patients)}) ---")
        for i, patient in enumerate(self._patients, 1):
            print(f"{i}. {patient.get_complete_info()}")

def demonstrate_system():
    print("=== CLINISOFT SYSTEM - DEMONSTRATION ===\n")
    
    clinic = Clinic("Marbella Clinic", "Lima, Peru")
    
    consulting_room1 = ConsultingRoom(101, "Cardiology")
    consulting_room2 = ConsultingRoom(102, "Urology")
    clinic.add_consulting_room(consulting_room1)
    clinic.add_consulting_room(consulting_room2)
    
    dr_garcia = Doctor("M001", "Carlos", "García", "cgarcia@marbellaclinic.com", 
                      "987654321", "Cardiology", 150.0)
    dra_rodriguez = Doctor("M002", "Ana", "Rodríguez", "arodriguez@marbellaclinic.com", 
                          "987654322", "Urology", 180.0)
    
    clinic.hire_doctor(dr_garcia)
    clinic.hire_doctor(dra_rodriguez)
    
    secretary_maria = Secretary("S001", "María", "López", "mlopez@marbellaclinic.com", 
                                 "987654323", "Morning", "Admission")
    clinic._secretaries.append(secretary_maria)
    
    print("\n1. INITIAL PATIENT SEARCH:")
    print("-" * 40)
    
    found_patient = clinic.find_patient_by_id("P001")
    if found_patient:
        print(f"✓ Patient found: {found_patient.get_complete_info()}")
    else:
        print("✗ No patient found with ID P001 (expected - not yet registered)")
    
    print("\n2. PATIENT REGISTRATION:")
    print("-" * 40)
    
    patient1 = Patient("P001", "Juan", "Pérez", "juan@email.com", "987654324", 
                        date(1980, 5, 15))
    patient2 = Patient("P002", "Laura", "Gómez", "laura@email.com", "987654325", 
                        date(1990, 8, 22))
    
    secretary_maria.register_patient(clinic, patient1)
    secretary_maria.register_patient(clinic, patient2)
    
    clinic.show_all_patients()
    
    print("\n3. SEARCH FOR REGISTERED PATIENTS:")
    print("-" * 40)
    
    found_patient = clinic.find_patient_by_id("P001")
    if found_patient:
        print(f"✓ Patient found: {found_patient.get_complete_info()}")
    else:
        print("✗ Patient not found")
    
    laura_patients = clinic.find_patient_by_name("Laura")
    print(f"✓ Patients found with 'Laura': {len(laura_patients)}")
    for p in laura_patients:
        print(f"  - {p.get_complete_info()}")
    
    print("\n4. APPOINTMENT SCHEDULING:")
    print("-" * 40)
    
    appointment1 = secretary_maria.schedule_medical_appointment(
        dr_garcia, patient1, date(2024, 1, 20), time(10, 0), "General consultation"
    )
    
    if appointment1:
        print(f"✓ Appointment scheduled: {appointment1.get_appointment_info()}")
    else:
        print("✗ Could not schedule appointment")
    
    print("\n5. POLYMORPHISM DEMONSTRATION:")
    print("-" * 40)
    
    people = [patient1, dr_garcia, secretary_maria]
    
    for person in people:
        print(f"→ {person.get_complete_info()}")
    
    print("\n6. REPORTS AND METRICS:")
    print("-" * 40)
    
    metrics = clinic.get_operational_metrics()
    print(f"Total patients: {metrics['total_patients']}")
    print(f"Total doctors: {metrics['total_doctors']}")
    print(f"Total consulting rooms: {metrics['total_consulting_rooms']}")
    print(f"Specialties: {', '.join(metrics['specialties'])}")
    
    print("\n7. PAYMENT CALCULATION (Recursive):")
    print("-" * 40)
    
    payment = dr_garcia.calculate_payment(date(2024, 1, 1), date(2024, 1, 31))
    print(f"Dr. García's payment: S/.{payment:.2f}")
    
    print("\n=== DEMONSTRATION COMPLETED ===")

def main_menu():
    clinic = Clinic("Marbella Clinic", "Lima, Peru")
    
    dr_example = Doctor("M001", "Carlos", "García", "cgarcia@marbellaclinic.com", 
                       "987654321", "Cardiology", 150.0)
    clinic.hire_doctor(dr_example)
    
    while True:
        print("\n" + "="*50)
        print("=== CLINISOFT MENU ===")
        print("1. Register patient")
        print("2. Search patient by ID")
        print("3. Search patient by name")
        print("4. View all patients")
        print("5. View clinic metrics")
        print("6. Schedule medical appointment")
        print("7. Demonstrate complete functionalities")
        print("8. Exit")
        print("="*50)
        
        option = input("Select an option: ").strip()
        
        if option == "1":
            print("\n--- REGISTER NEW PATIENT ---")
            patient_id = input("Patient ID: ").strip()
            name = input("Name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            birth_date = input("Birth date (YYYY-MM-DD): ").strip()
            
            try:
                birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
                new_patient = Patient(patient_id, name, last_name, email, phone, birth_date_obj)
                
                if clinic.register_patient(new_patient):
                    print("✓ Patient registered successfully")
                else:
                    print("✗ Error: Patient with that ID already exists")
                    
            except ValueError:
                print("✗ Error: Incorrect date format. Use YYYY-MM-DD")
        
        elif option == "2":
            print("\n--- SEARCH PATIENT BY ID ---")
            search_id = input("Patient ID to search: ").strip()
            patient = clinic.find_patient_by_id(search_id)
            
            if patient:
                print(f"✓ Patient found: {patient.get_complete_info()}")
            else:
                print("✗ Patient not found")
        
        elif option == "3":
            print("\n--- SEARCH PATIENT BY NAME ---")
            search_name = input("Name to search: ").strip()
            patients = clinic.find_patient_by_name(search_name)
            
            if patients:
                print(f"✓ Found {len(patients)} patients:")
                for p in patients:
                    print(f"  - {p.get_complete_info()}")
            else:
                print("✗ No patients found")
        
        elif option == "4":
            clinic.show_all_patients()
        
        elif option == "5":
            metrics = clinic.get_operational_metrics()
            print("\n--- CLINIC METRICS ---")
            for key, value in metrics.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        elif option == "6":
            print("\n--- SCHEDULE MEDICAL APPOINTMENT ---")
            if not clinic._patients:
                print("✗ First register patients")
                continue
                
            patient_id = input("Patient ID: ").strip()
            patient = clinic.find_patient_by_id(patient_id)
            
            if not patient:
                print("✗ Patient not found")
                continue
            
            doctor = dr_example
            date_str = input("Appointment date (YYYY-MM-DD): ").strip()
            time_str = input("Appointment time (HH:MM): ").strip()
            consultation_type = input("Consultation type: ").strip()
            
            try:
                appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                appointment_time = datetime.strptime(time_str, "%H:%M").time()
                
                temp_secretary = Secretary("S999", "Temp", "Temp", "temp@temp.com", 
                                           "000000000", "Morning", "Temporary")
                
                appointment = temp_secretary.schedule_medical_appointment(doctor, patient, appointment_date, appointment_time, consultation_type)
                
                if appointment:
                    print(f"✓ Appointment scheduled successfully:")
                    print(f"  {appointment.get_appointment_info()}")
                else:
                    print("✗ Could not schedule appointment (doctor not available)")
                    
            except ValueError as e:
                print(f"✗ Error in date/time format: {e}")
        
        elif option == "7":
            demonstrate_system()
        
        elif option == "8":
            print("Thank you for using CliniSoft!")
            break
        
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    print("Welcome to CliniSoft Clinical Management System")
    print("Developed for Marbella Clinic")
    print("=" * 50)
    
    use_demo = input("Do you want to see the automatic demonstration? (y/n): ").lower().strip()
    if use_demo == 'y':
        demonstrate_system()
    
    use_menu = input("\nDo you want to use the interactive menu? (y/n): ").lower().strip()
    if use_menu == 'y':
        main_menu()
    else:
        print("Goodbye!")