# Virus simulation based on a NetLogo model 

Course: IE0499 II-2020

Authors: 
- James Sibaja B77342

## Dependencias
- Python 3.6
- Django 2.2.11
- 
- VIPS


## Instalar dependencias

```bash
make install
```

## Correr en el sevidro local 

```bash
make run
```
### Considerations 

infectiousness and chance_of_recovery are percentages given as integer numbers from 0 to 100. 

## Crear placa virtual de una archivo svs de internet 

```bash
make slide ARGS="<url del archivo svs>" ARGS2="<nombre del directorio a crear>"
```
