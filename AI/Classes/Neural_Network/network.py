import random
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import os

FeatureVector = dict[str, str]

# Konwersje

FEATURES = [
    "amount_waiting",
    "cook_has_available_food",
    "has_carrying_food",
    "has_pending_orders",
    "order_list_sent",
    "any_client_wants_order",
    "any_client_waiting_for_food",
    "cook_has_pending_orders",
]

ACTIONS = [
    "idle",
    "take_order",
    "take_food",
    "deliver_food",
    "give_order_list",
]

ACTION_TO_ID = {
    action: i for i, action in enumerate(ACTIONS)
}

ID_TO_ACTION = {
    i: action for action, i in ACTION_TO_ID.items()
}


def bool_to_str(value: bool) -> str:
    return "yes" if value else "no"


def state_to_tensor(state):

    values=[]

    for feature in FEATURES:

        value = state[feature]

        if feature == "amount_waiting":
            values.append(float(value))

        else:
            values.append(
                1.0 if value=="yes"
                else 0.0
            )

    return torch.tensor(values,dtype=torch.float32)

# Logika generująca poprawne decyzje

def decision_logic(state: FeatureVector) -> str:

    if state["has_carrying_food"] == "yes":
        return "deliver_food"

    elif state["cook_has_available_food"] == "yes":
        return "take_food"

    elif int(state["amount_waiting"]) > 2:
        return "give_order_list"

    elif state["any_client_wants_order"]=="yes":
        return "take_order"

    elif state["has_pending_orders"] == "yes":
        return "give_order_list"

    return "idle"


# Generowanie datasetu
# >1000 próbek na klasę

def generate_dataset(samples_per_class=1000):

    X = []
    y = []

    saved_rows = []

    class_counts = {action: 0 for action in ACTIONS}

    while min(class_counts.values()) < samples_per_class:

        state = {
            "amount_waiting":
                str(random.randint(0,10)),

            "cook_has_available_food":
                random.choice(["yes","no"]),

            "has_carrying_food":
                random.choice(["yes","no"]),

            "has_pending_orders":
                random.choice(["yes","no"]),

            "order_list_sent":
                random.choice(["yes","no"]),

            "any_client_wants_order":
                random.choice(["yes","no"]),

            "any_client_waiting_for_food":
                random.choice(["yes","no"]),

            "cook_has_pending_orders":
                random.choice(["yes","no"])
        }

        label = decision_logic(state)
        saved_rows.append(f"{state} -> {label}")

        if class_counts[label] >= samples_per_class:
            continue

        x = state_to_tensor(state)

        X.append(x)
        y.append(ACTION_TO_ID[label])

        class_counts[label] += 1

    X = torch.stack(X)
    y = torch.tensor(y)

    # zapis datasetu do dataset.txt

    current_dir = os.path.dirname(os.path.abspath(__file__))

    dataset_path = os.path.join(current_dir,"dataset.txt")

    with open(dataset_path,"w",encoding="utf-8") as file:
        file.write("\n".join(saved_rows))

    print(f"Dataset zapisany: {dataset_path}")

    return X, y


# Sieć neuronowa

class WaiterNeuralNetwork(nn.Module):

    def __init__(self):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(8, 32),
            nn.ReLU(),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 5)

        )

    def forward(self, x):
        return self.network(x)


# Klasa agenta

class WaiterAI:

    def __init__(self):

        self.model = WaiterNeuralNetwork()

    def train(self):

        X, y = generate_dataset(samples_per_class=1000)

        dataset = TensorDataset(X, y)

        loader = DataLoader(dataset, batch_size=64, shuffle=True)

        criterion = nn.CrossEntropyLoss()

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

        epochs = 20

        for epoch in range(epochs):

            total_loss = 0

            for batch_x, batch_y in loader:

                prediction = self.model(batch_x)

                loss = criterion(prediction, batch_y)

                #sprawdzanie pwływu na błąd, dodanie poprawionych wag i usunięcie poprzednich
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            print(f"Epoch {epoch+1}: "f"{total_loss:.4f}")

        current_dir = os.path.dirname(os.path.abspath(__file__))

        model_path = os.path.join(current_dir,"waiter_model.pth")

        torch.save(self.model.state_dict(),model_path)

        print(f"Model zapisany: {model_path}")

    def load(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))

        model_path = os.path.join(current_dir,"waiter_model.pth")

        self.model.load_state_dict(torch.load(model_path))

        self.model.eval()

    def predict(self, state: FeatureVector):

        x = state_to_tensor(state).unsqueeze(0)

        with torch.no_grad():

            prediction = self.model(x)

            action_id = torch.argmax(prediction, dim=1).item()

        return ID_TO_ACTION[action_id]


# Test

if __name__ == "__main__":

    ai = WaiterAI()

    ai.train()

    test_state = {

        "amount_waiting":"3",
        "cook_has_available_food":"no",
        "has_carrying_food":"yes",
        "has_pending_orders":"no",
        "order_list_sent":"no",
        "any_client_wants_order":"no",
        "any_client_waiting_for_food":"yes",
        "cook_has_pending_orders":"no"
    }

    decision = ai.predict(test_state)

    print("Decyzja:",decision)