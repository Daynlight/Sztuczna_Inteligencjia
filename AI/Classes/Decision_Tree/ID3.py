import math
from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import random

FeatureVector = Dict[str, str]
DataSet = List[FeatureVector]
Labels = List[str]

# Liczenie entropii dla danych atrybutów

def _entropy(labels: Labels) -> float:
    total = len(labels)
    if total == 0:
        return 0.0

    counts = Counter(labels)
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy

# Dzielenie zbiorów danych

def _split_dataset(dataset: DataSet, labels: Labels, attribute: str) -> Dict[str, tuple[DataSet, Labels]]:
    partitions: Dict[str, tuple[DataSet, Labels]] = {}
    for row, label in zip(dataset, labels):
        value = row.get(attribute, "")
        subset, subset_labels = partitions.setdefault(value, ([], []))
        subset.append(row)
        subset_labels.append(label)
    return partitions

# Liczenie ile informacji daje dany atrybut

def _information_gain(dataset: DataSet, labels: Labels, attribute: str) -> float:
    base_entropy = _entropy(labels)
    partitions = _split_dataset(dataset, labels, attribute)

    partition_entropy = 0.0
    total = len(labels)
    for subset, subset_labels in partitions.values():
        weight = len(subset_labels) / total
        partition_entropy += weight * _entropy(subset_labels)

    return base_entropy - partition_entropy

# Znajdowanie najczęściej występującej etykiety

def _majority_label(labels: Labels) -> Optional[str]:
    if not labels:
        return None
    return Counter(labels).most_common(1)[0][0]


@dataclass
class DecisionTreeNode:
    attribute: Optional[str] = None
    label: Optional[str] = None
    children: Dict[str, "DecisionTreeNode"] = None

    def __post_init__(self) -> None:
        if self.children is None:
            self.children = {}

    def predict(self, sample: FeatureVector) -> Optional[str]:
        if self.label is not None:
            return self.label

        if self.attribute is None:
            return None

        value = sample.get(self.attribute)
        child = self.children.get(value)
        if child is not None:
            return child.predict(sample)

        # fallback to majority child label when value not seen during training
        if self.children:
            return _majority_label([child.label for child in self.children.values() if child.label is not None])
        return None


class DecisionTreeClassifier:
    def __init__(self) -> None:
        self.root: Optional[DecisionTreeNode] = None
        self.features: List[str] = []

    def fit(self, dataset: DataSet, labels: Labels, features: List[str]) -> None:
        self.features = features
        default_label = _majority_label(labels)
        self.root = self._build_tree(dataset, labels, features, default_label)

    def _build_tree(self, dataset: DataSet, labels: Labels, attributes: List[str], default_label: Optional[str]) -> DecisionTreeNode:
        if not labels:
            return DecisionTreeNode(label=default_label)

        if len(set(labels)) == 1:
            return DecisionTreeNode(label=labels[0])

        if not attributes:
            return DecisionTreeNode(label=_majority_label(labels))

        gains = [(attribute, _information_gain(dataset, labels, attribute)) for attribute in attributes]
        best_attribute, best_gain = max(gains, key=lambda item: item[1])

        if best_gain <= 0:
            return DecisionTreeNode(label=_majority_label(labels))

        node = DecisionTreeNode(attribute=best_attribute)
        new_default_label = _majority_label(labels)
        remaining_attributes = [attribute for attribute in attributes if attribute != best_attribute]

        for value, (subset, subset_labels) in _split_dataset(dataset, labels, best_attribute).items():
            child = self._build_tree(subset, subset_labels, remaining_attributes, new_default_label)
            node.children[value] = child

        return node

    def predict(self, sample: FeatureVector) -> Optional[str]:
        if self.root is None:
            return None
        return self.root.predict(sample)


def tree_to_string(node: DecisionTreeNode, depth: int = 0) -> str:
    indent = "  " * depth
    if node.label is not None:
        return f"{indent}Label: {node.label}\n"

    lines = [f"{indent}[{node.attribute}]"]
    for value, child in sorted(node.children.items()):
        lines.append(f"{indent}  {value} ->")
        lines.append(tree_to_string(child, depth + 2))
    return "\n".join(lines)


def save_tree_to_file(tree: DecisionTreeClassifier, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as tree_file:
        tree_file.write(tree_to_string(tree.root))



def build_waiter_decision_tree() -> DecisionTreeClassifier:
    features = [
        "all_waiting",
        "cook_has_available_food",
        "has_carrying_food",
        "has_pending_orders",
        "order_list_sent",
        "any_client_wants_order",
        "any_client_waiting_for_food",
        "cook_has_pending_orders",
    ]

    dataset: DataSet = []
    labels: Labels = []

    # Generowanie lekkiego szumu do danych dla różnorodności

    def noisy_decision(state: dict[str, str]) -> str:
        actions = ["idle", "take_order", "take_food", "deliver_food", "give_order_list"]

        if state["has_carrying_food"] == "yes":
            base = "deliver_food"
        elif state["cook_has_available_food"] == "yes":
            base = "take_food"
        elif state["any_client_wants_order"] == "yes":
            base = "take_order"
        elif state["has_pending_orders"] == "yes":
            base = "give_order_list"
        else:
            base = "idle"

        if random.random() < 0.1:
            return random.choice(actions)

        return base
    
    for all_waiting in ["no", "yes"]:
        for cook_available in ["no", "yes"]:
            for carrying in ["no", "yes"]:
                for pending_orders in ["no", "yes"]:
                    for order_list_sent in ["no", "yes"]:
                        for wants_order in ["no", "yes"]:
                            for waiting_for_food in ["no", "yes"]:
                                for cook_pending in ["no", "yes"]:

                                    state = {
                                        "all_waiting": all_waiting,
                                        "cook_has_available_food": cook_available,
                                        "has_carrying_food": carrying,
                                        "has_pending_orders": pending_orders,
                                        "order_list_sent": order_list_sent,
                                        "any_client_wants_order": wants_order,
                                        "any_client_waiting_for_food": waiting_for_food,
                                        "cook_has_pending_orders": cook_pending,
                                    }

                                    dataset.append(state)
                                    labels.append(noisy_decision(state))  

    classifier = DecisionTreeClassifier()
    classifier.fit(dataset, labels, features)
    dataset_file_path = "AI/Classes/Decision_Tree/dataset.txt"
    try:
        with open(dataset_file_path, "w", encoding="utf-8") as dataset_file:
            for row, label in zip(dataset, labels):
                dataset_file.write(f"{row} -> {label}\n")
    except IOError:
        dataset_file_path = "Classes/Decision_Tree/dataset.txt"
        with open(dataset_file_path, "w", encoding="utf-8") as dataset_file:
            for row, label in zip(dataset, labels):
                dataset_file.write(f"{row} -> {label}\n")
    print(f"Dataset saved to {dataset_file_path}")

    tree_file_path = "AI/Classes/Decision_Tree/decision_tree.txt"
    try:
        save_tree_to_file(classifier, tree_file_path)
    except IOError:
        tree_file_path = "Classes/Decision_Tree/decision_tree.txt"
        save_tree_to_file(classifier, tree_file_path)
    print(f"Decision tree saved to {tree_file_path}")
    return classifier


def bool_to_str(value: bool) -> str:
    return "yes" if value else "no"

