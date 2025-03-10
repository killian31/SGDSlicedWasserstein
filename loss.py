import torch
import torch.nn as nn
import torch.nn.functional as F


def sw_loss(true_distribution, generated_distribution, num_projections=100):
    """
    Compute the Sliced Wasserstein Distance (SWD) between two distributions.

    Args:
        true_distribution (Tensor): Samples from the real distribution, shape [batch_size, feature_dim].
        generated_distribution (Tensor): Samples from the generator, shape [batch_size, feature_dim].
        num_projections (int): Number of random projection directions.

    Returns:
        Tensor: Sliced Wasserstein distance.
    """
    _, feature_dim = true_distribution.shape

    # Sample random projection directions
    theta = torch.randn(feature_dim, num_projections, device=true_distribution.device)
    theta = F.normalize(theta, dim=0)  # Normalize to unit norm

    # Project the samples
    proj_true = true_distribution @ theta  # Shape: [batch_size, num_projections]
    proj_fake = generated_distribution @ theta  # Shape: [batch_size, num_projections]

    # Sort projections along each direction
    proj_true_sorted, _ = torch.sort(proj_true, dim=0)
    proj_fake_sorted, _ = torch.sort(proj_fake, dim=0)

    # Compute Wasserstein-2 distance (L2 norm of sorted differences)
    sliced_wasserstein_distance = torch.mean((proj_true_sorted - proj_fake_sorted) ** 2)

    return sliced_wasserstein_distance


class SWDLoss(nn.Module):
    def __init__(self, num_projections=100):
        """
        Initialize the Sliced Wasserstein Distance (SWD) loss.

        Args:
            num_projections (int): Number of random projection directions.
        """
        super(SWDLoss, self).__init__()
        self.num_projections = num_projections

    def forward(self, true_distribution, generated_distribution):
        """
        Compute the Sliced Wasserstein Distance (SWD) between two distributions.

        Args:
            true_distribution (Tensor): Samples from the real distribution, shape [batch_size, feature_dim].
            generated_distribution (Tensor): Samples from the generator, shape [batch_size, feature_dim].

        Returns:
            Tensor: Sliced Wasserstein distance.
        """
        return sw_loss(true_distribution, generated_distribution, self.num_projections)
