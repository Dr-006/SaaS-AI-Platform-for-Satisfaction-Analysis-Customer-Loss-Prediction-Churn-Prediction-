# backend/app/routes/clients.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ClientCreate, ClientOut
from app.models import Client
from app.database import SessionLocal

router = APIRouter(prefix="/clients", tags=["clients"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[ClientOut])
def list_clients(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Client).order_by(Client.id.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    from app.services import churn_service
    from app.models import Prediction

    db_client = Client(
        name=client.name,
        email=client.email,
        tenure=client.tenure,
        monthly_charges=client.monthly_charges,
    )

    # Quick churn prediction with available fields
    try:
        input_data = {
            "tenure": client.tenure,
            "MonthlyCharges": client.monthly_charges,
        }
        result = churn_service.predict_churn(input_data)
        db_client.churn_probability = result["probability"]
        db_client.churn_prediction = result["prediction"]

        # Save prediction to history
        pred = Prediction(probability=result["probability"], prediction=result["prediction"])
        db.add(pred)
    except Exception:
        pass

    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.post("/sync-from-app1", response_model=ClientOut)
def sync_client_from_app1(client_data: dict, db: Session = Depends(get_db)):
    """
    Endpoint pour synchroniser automatiquement un client analysé depuis app1-gestionnaire
    """
    from app.models import Prediction
    
    print(f"🔄 Synchronisation client depuis app1-gestionnaire")
    print(f"📥 Données reçues: {client_data}")
    
    # Extraire les données du client
    name = client_data.get("name", f"Client {client_data.get('customerId', 'Unknown')}")
    email = client_data.get("email")
    tenure = client_data.get("tenure")
    monthly_charges = client_data.get("monthlyCharges")
    
    # Extraire les résultats de prédiction
    churn_probability = client_data.get("churn_probability")
    churn_prediction = client_data.get("churn_prediction")
    
    print(f"👤 Client: {name} | Email: {email}")
    print(f"📊 Prédiction: {churn_prediction} | Probabilité: {churn_probability}")
    
    # Vérifier si le client existe déjà (par email ou nom)
    existing_client = None
    if email:
        existing_client = db.query(Client).filter(Client.email == email).first()
        if existing_client:
            print(f"♻️  Client existant trouvé: #{existing_client.id}")
    
    if existing_client:
        # Mettre à jour le client existant
        existing_client.tenure = tenure
        existing_client.monthly_charges = monthly_charges
        existing_client.churn_probability = churn_probability
        existing_client.churn_prediction = churn_prediction
        db_client = existing_client
        print(f"✏️  Mise à jour du client #{db_client.id}")
    else:
        # Créer un nouveau client
        db_client = Client(
            name=name,
            email=email,
            tenure=tenure,
            monthly_charges=monthly_charges,
            churn_probability=churn_probability,
            churn_prediction=churn_prediction,
        )
        db.add(db_client)
        print(f"➕ Création d'un nouveau client")
    
    # Enregistrer la prédiction dans l'historique
    if churn_probability is not None and churn_prediction is not None:
        pred = Prediction(
            probability=churn_probability,
            prediction=churn_prediction
        )
        db.add(pred)
        print(f"💾 Prédiction enregistrée dans l'historique")
    
    db.commit()
    db.refresh(db_client)
    
    print(f"✅ Synchronisation terminée - Client #{db_client.id}")
    
    return db_client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message": "Client deleted"}
