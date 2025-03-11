import matplotlib.pyplot as plt
import torch
import json

def plot_distributions(
    source, generated, target, title="Distribution Comparison", filename=None
):
    """
    Plot four distributions side by side:
      - Left: Source distribution
      - Middle Left: Generated distribution (output of model)
      - Middle Right: Target distribution
      - Right: Generated vs Target distribution

    Args:
        source (Tensor or np.array): Samples from the source distribution, shape [n_samples, 2].
        generated (Tensor or np.array): Samples generated by the model, shape [n_samples, 2].
        target (Tensor or np.array): Samples from the target distribution, shape [n_samples, 2].
        title (str): Overall title for the figure.
        filename (str, optional): If provided, the figure is saved to this file.
    """
    if torch.is_tensor(source):
        source = source.cpu().detach().numpy()
    if torch.is_tensor(generated):
        generated = generated.cpu().detach().numpy()
    if torch.is_tensor(target):
        target = target.cpu().detach().numpy()

    fig, axes = plt.subplots(1, 4, figsize=(12, 6))

    axes[0].scatter(source[:, 0], source[:, 1], s=15, alpha=0.7, edgecolors="k")
    axes[0].set_title("Source Distribution", fontsize=14)
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    axes[1].scatter(generated[:, 0], generated[:, 1], s=15, alpha=0.7, edgecolors="k")
    axes[1].set_title("Generated Distribution", fontsize=14)
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Y")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    axes[2].scatter(target[:, 0], target[:, 1], s=15, alpha=0.7, edgecolors="k")
    axes[2].set_title("Target Distribution", fontsize=14)
    axes[2].set_xlabel("X")
    axes[2].set_ylabel("Y")
    axes[2].grid(True, linestyle="--", alpha=0.6)

    axes[3].scatter(
        generated[:, 0],
        generated[:, 1],
        s=15,
        alpha=0.7,
        color="tab:orange",
        label="Generated",
    )
    axes[3].scatter(
        target[:, 0], target[:, 1], s=15, alpha=0.7, color="tab:green", label="Target"
    )
    axes[3].legend()
    axes[3].set_title("Generated vs Target", fontsize=14)
    axes[3].set_xlabel("X")
    axes[3].set_ylabel("Y")
    axes[3].grid(True, linestyle="--", alpha=0.6)

    fig.suptitle(title, fontsize=16, y=1.02)
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.show()


def plot_model_results(
    model,
    source_dataset,
    target_dataset,
    device,
    title="Distribution Comparison",
    filename=None,
):
    """
    Generate predictions using the trained model on the source dataset and plot the
    source, generated, and target distributions side by side.

    Args:
        model (torch.nn.Module): The trained generator model.
        source_dataset (torch.utils.data.Dataset or Tensor): Dataset containing source samples.
        target_dataset (torch.utils.data.Dataset or Tensor): Dataset containing target samples.
        device (torch.device): Device for running the model.
        title (str): Overall title for the figure.
        filename (str, optional): If provided, save the figure to this file.
    """

    def dataset_to_tensor(dataset):
        if torch.is_tensor(dataset):
            return dataset
        samples = []
        for i in range(len(dataset)):
            sample = dataset[i]
            if isinstance(sample, (tuple, list)):
                sample = sample[0]
            samples.append(sample)
        return torch.stack(samples)

    source_tensor = dataset_to_tensor(source_dataset)
    target_tensor = dataset_to_tensor(target_dataset)

    model.eval()
    with torch.no_grad():
        generated_tensor = model(source_tensor.to(device)).cpu()

    plot_distributions(
        source_tensor, generated_tensor, target_tensor, title=title, filename=filename
    )

def plot_loss(training_history_path, filename=None):
    """
    Plot the training and validation loss from a training history file.

    Args:
        training_history_path (str): Path to the training history file.
    """
    with open(training_history_path, "r") as file:
        file_contents = file.read()
        history = json.loads(file_contents)

    train_loss = history["train_loss"]
    valid_loss = history["valid_loss"]

    plt.figure(figsize=(10, 5))
    plt.plot(train_loss, label="Train Loss", color="blue", alpha=0.8)
    plt.plot(valid_loss, label="Valid Loss", color="red", alpha=0.8)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Loss", fontsize=12)
    plt.title("Training and Validation Loss", fontsize=14)
    plt.legend()
    plt.grid(True)
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.show()