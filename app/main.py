from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .database import SessionLocal, Passenger
import qrcode, os
from pyzbar.pyzbar import decode
from PIL import Image

# Create the FastAPI app instance
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Join the queue
@app.post("/join_queue/")
def join_queue(name: str, phone: str, db: Session = Depends(get_db)):
    queue_number = db.query(Passenger).count() + 1
    passenger = Passenger(name=name, phone=phone, queue_number=queue_number)

    # Generate QR code
    qr_data = f"Passenger: {name}, Queue Number: {queue_number}"
    qr_path = f"qr_codes/{queue_number}.png"
    os.makedirs("qr_codes", exist_ok=True)
    qrcode.make(qr_data).save(qr_path)

    passenger.qr_code_path = qr_path
    db.add(passenger)
    db.commit()

    return {"queue_number": queue_number, "qr_code": qr_path}

# 2. Check queue status
@app.get("/queue_status/{queue_number}")
def queue_status(queue_number: int, db: Session = Depends(get_db)):
    passenger = db.query(Passenger).filter(Passenger.queue_number == queue_number).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return {"checked_in": passenger.checked_in}

# 3. Check-in using QR code
@app.post("/check_in_qr/")
def check_in_qr(qr_code: UploadFile = File(...), db: Session = Depends(get_db)):
    image = Image.open(qr_code.file)
    decoded = decode(image)

    if not decoded:
        raise HTTPException(status_code=400, detail="Invalid QR Code")

    data = decoded[0].data.decode("utf-8")
    queue_number = int(data.split(",")[1].split(":")[1].strip())

    passenger = db.query(Passenger).filter(Passenger.queue_number == queue_number).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")

    passenger.checked_in = True
    db.commit()

    return {"message": "Check-in successful"}
