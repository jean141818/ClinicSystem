# CliniSoft - Clinical Management System

A comprehensive clinical management system built with Python that handles patient records, medical appointments, doctor schedules, and clinic operations using object-oriented programming principles and custom data structures.

## Features

### Core Functionality
- **Patient Management**: Register and search patients using binary and sequential search algorithms
- **Medical Appointments**: Schedule and manage appointments with availability checking
- **Doctor Management**: Handle doctor information, specialties, and consultation fees
- **Medical Records**: Maintain complete patient medical history using linked lists
- **Clinic Operations**: Manage consulting rooms, staff, and operational metrics

### Advanced Features
- **Object-Oriented Design**: Full implementation of inheritance, polymorphism, and composition
- **Custom Data Structures**: Linked lists for medical history and appointment scheduling
- **Search Algorithms**: Binary search for patient IDs and sequential search for names
- **Recursive Algorithms**: For medical history display and payment calculations
- **Polymorphic Behavior**: Unified interface for different person types (patients, doctors, secretaries)

## System Architecture

### Main Classes

#### Person Hierarchy
- `Person`: Base class with common attributes
- `Patient`: Manages patient data and medical history
- `Doctor`: Handles doctor information and appointment scheduling
- `Secretary`: Manages administrative tasks and patient registration

#### Data Structures
- `ConsultationList`: Linked list for patient medical history
- `AppointmentList`: Linked list for doctor appointment scheduling
- `ConsultingRoom`: Manages clinic consulting room resources

#### Management Classes
- `Clinic`: Main system controller with search and management operations
- `Consultation`: Represents medical consultations
- `Appointment`: Handles appointment scheduling and status

