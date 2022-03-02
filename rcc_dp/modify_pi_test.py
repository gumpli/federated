# Copyright 2021, Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for modify pi."""

from absl.testing import absltest
import numpy as np

from rcc_dp import modify_pi
from rcc_dp.mean_estimation import get_parameters
from rcc_dp.mean_estimation import miracle


class ModifyPiTest(absltest.TestCase):

  def test_tilde_pi_is_a_distribution(self):
    """Test whether every distribution generated by modify_all sums to 1."""
    budget = 0.5
    for d in [100, 200]:
      for number_candidates in [2**4, 2**5]:
        for epsilon in [2, 3]:
          x = np.random.normal(0, 1, (d, 1))
          x = np.divide(x, np.linalg.norm(x, axis=0).reshape(1, -1))
          c1, c2, _, gamma = get_parameters.get_parameters_unbiased_miracle(
              epsilon, d, number_candidates, budget)
          _, _, pi = miracle.encoder(0, x[:, 0], number_candidates, c1, c2,
                                     gamma)
          eta = epsilon / 2
          pi_all = modify_pi.modify_pi(pi, eta, epsilon,
                                       c1 / (np.exp(epsilon / 2)))
          self.assertLessEqual(len(pi_all), 3)
          for distribution in pi_all:
            self.assertLessEqual(np.abs(np.sum(distribution) - 1), 0.0001)

  def test_tilde_pi_is_private(self):
    """Test whether tilde pi satisfies the DP constraint."""
    budget = 0.5
    for d in [100, 200]:
      for number_candidates in [2**4, 2**5]:
        for epsilon in [2, 3]:
          x = np.random.normal(0, 1, (d, 1))
          x = np.divide(x, np.linalg.norm(x, axis=0).reshape(1, -1))
          c1, c2, _, gamma = get_parameters.get_parameters_unbiased_miracle(
              epsilon, d, number_candidates, budget)
          _, _, pi = miracle.encoder(0, x[:, 0], number_candidates, c1, c2,
                                     gamma)
          eta = epsilon / 2
          pi_all = modify_pi.modify_pi(pi, eta, epsilon,
                                       c1 / (np.exp(epsilon / 2)))
          self.assertLessEqual(np.max(pi_all[-1]), c1 / number_candidates)
          self.assertLessEqual(c1 * np.exp(-epsilon) / number_candidates,
                               np.min(pi_all[-1]) + 1e-6)

  def test_convergence(self):
    """Test whether modify_pi converges in at-most 3 iterations as expected."""
    budget = 0.5
    for d in [100, 200]:
      for number_candidates in [2**4, 2**5]:
        for epsilon in [2, 3]:
          x = np.random.normal(0, 1, (d, 1))
          x = np.divide(x, np.linalg.norm(x, axis=0).reshape(1, -1))
          c1, c2, _, gamma = get_parameters.get_parameters_unbiased_miracle(
              epsilon, d, number_candidates, budget)
          _, _, pi = miracle.encoder(0, x[:, 0], number_candidates, c1, c2,
                                     gamma)
          eta = epsilon / 2
          pi_all = modify_pi.modify_pi(pi, eta, epsilon,
                                       c1 / (np.exp(epsilon / 2)))
          self.assertLessEqual(len(pi_all), 3)


if __name__ == "__main__":
  absltest.main()
