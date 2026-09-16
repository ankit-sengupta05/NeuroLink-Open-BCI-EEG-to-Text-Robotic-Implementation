# 105-Channel EGI HydroCel-128 Coordinate-Based Scalp and Functional Candidate Map

> **Disclaimer**: Electrode labels represent nominal scalp-coordinate regions and task-related hypotheses. They do not establish direct correspondence between any electrode and a specific cortical area. Functional assignments must be validated using participant-specific electrode digitization, anatomical registration, source localization, and task-based statistical analysis.

## Notes

- **Cz stand-in**: The 128-net has no vertex electrode (Cz). E55 serves as the midline vertex stand-in.
- **FpZ/Frontal-pole**: E17 serves as the frontal-pole electrode.
- **Coordinates**: Expressed in cm, normalized from the MNE standard montage.

## Functional Envelopes

- **Left inferior-frontal language-related candidate (Broca's candidate)**: `x <= -4.0, y >= 1.0, z >= -1.0`
- **Left lateral/superior-temporal language-related candidate (Wernicke's candidate)**: `x <= -4.0, y < 1.0, z < 5.0`
- **Right inferior-frontal homolog candidate**: `x >= 4.0, y >= 1.0, z >= -1.0`
- **Medial frontal speech-preparation candidate (pre-SMA/SMA candidate)**: `|x| <= 2.0, y >= 2.0, z >= 5.0`

| Electrode     | Original Num | x (cm) | y (cm) | z (cm) | Scalp Region                   | Functional Candidate Hypothesis                 | Confidence                          |
| :------------ | :----------- | :----- | :----- | :----- | :----------------------------- | :---------------------------------------------- | :---------------------------------- |
| **E1**        | 1            | 6.27   | 5.98   | -2.79  | Right Lateral-temporal border  | -                                               | Medium                              |
| **E2**        | 2            | 5.73   | 7.26   | 0.33   | Right Frontal                  | Right inferior-frontal homolog                  | Medium                              |
| **E3**        | 3            | 4.18   | 8.27   | 3.32   | Right Frontal                  | Right inferior-frontal homolog                  | Medium                              |
| **E4**        | 4            | 3.11   | 7.74   | 5.40   | Right Frontal                  | -                                               | Medium                              |
| **E5**        | 5            | 1.60   | 6.16   | 7.38   | Right Frontal                  | Medial frontal speech-preparation               | Medium                              |
| **E6**        | 6            | 0.00   | 4.12   | 8.54   | Midline Frontal                | Medial frontal speech-preparation               | Medium                              |
| **E7**        | 7            | -1.33  | 1.69   | 9.14   | Left Central                   | -                                               | Medium                              |
| **E9**        | 9            | 2.92   | 9.62   | 1.18   | Right Frontal                  | -                                               | Medium                              |
| **E10**       | 10           | 1.98   | 9.43   | 3.45   | Right Frontal                  | -                                               | Medium                              |
| **Fz (E11)**  | 11           | 0.00   | 8.62   | 5.46   | Midline Frontal                | Medial frontal speech-preparation               | High (nominal 10-10 correspondence) |
| **E12**       | 12           | -1.60  | 6.16   | 7.38   | Left Frontal                   | Medial frontal speech-preparation               | Medium                              |
| **E13**       | 13           | -2.64  | 3.52   | 8.24   | Left Frontal                   | -                                               | Medium                              |
| **E15**       | 15           | 0.00   | 9.84   | 1.44   | Midline Frontal                | -                                               | Medium                              |
| **E16**       | 16           | 0.00   | 9.83   | 3.36   | Midline Frontal                | -                                               | Medium                              |
| **E17**       | 17           | 0.00   | 10.04  | -2.39  | Midline Frontal (Frontal-pole) | -                                               | Medium                              |
| **E18**       | 18           | -1.98  | 9.43   | 3.45   | Left Frontal                   | -                                               | Medium                              |
| **E19**       | 19           | -3.11  | 7.74   | 5.40   | Left Frontal                   | -                                               | Medium                              |
| **E20**       | 20           | -4.14  | 5.55   | 6.43   | Left Frontal                   | Left inferior-frontal language-related          | Medium                              |
| **E22**       | 22           | -2.92  | 9.62   | 1.18   | Left Frontal                   | -                                               | Medium                              |
| **E23**       | 23           | -4.18  | 8.27   | 3.32   | Left Frontal                   | Left inferior-frontal language-related          | Medium                              |
| **E24**       | 24           | -4.83  | 6.52   | 4.73   | Left Frontal                   | Left inferior-frontal language-related          | Medium                              |
| **E26**       | 26           | -5.73  | 7.26   | 0.33   | Left Frontal                   | Left inferior-frontal language-related          | Medium                              |
| **E27**       | 27           | -6.15  | 5.90   | 3.07   | Left Frontal                   | Left inferior-frontal language-related          | Medium                              |
| **E28**       | 28           | -6.01  | 4.50   | 5.01   | Left Frontal                   | Left inferior-frontal language-related          | Medium                              |
| **E29**       | 29           | -5.16  | 2.92   | 6.82   | Left Central                   | Left inferior-frontal language-related          | Medium                              |
| **E30**       | 30           | -4.00  | 1.04   | 8.26   | Left Central                   | Left inferior-frontal language-related          | Medium                              |
| **E31**       | 31           | -2.12  | -0.74  | 9.27   | Left Central                   | -                                               | Medium                              |
| **E32**       | 32           | -6.27  | 5.98   | -2.79  | Left Lateral-temporal border   | -                                               | Medium                              |
| **E33**       | 33           | -6.93  | 4.47   | -0.39  | Left Lateral-temporal border   | Left inferior-frontal language-related          | Medium                              |
| **E34**       | 34           | -7.39  | 3.21   | 2.63   | Left Lateral-temporal border   | Left inferior-frontal language-related          | Medium                              |
| **E35**       | 35           | -6.94  | 1.61   | 5.13   | Left Central                   | Left inferior-frontal language-related          | Medium                              |
| **C3 (E36)**  | 36           | -5.93  | 0.31   | 6.91   | Left Central                   | -                                               | High (nominal 10-10 correspondence) |
| **E37**       | 37           | -4.23  | -1.64  | 8.41   | Left Central                   | -                                               | Medium                              |
| **E38**       | 38           | -7.09  | 3.91   | -3.63  | Left Lateral-temporal border   | -                                               | Medium                              |
| **E39**       | 39           | -7.79  | 0.92   | -0.96  | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E40**       | 40           | -8.00  | 0.03   | 2.32   | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E41**       | 41           | -7.48  | -0.87  | 4.98   | Left Central                   | Left lateral/superior-temporal language-related | Medium                              |
| **E42**       | 42           | -6.45  | -2.53  | 6.50   | Left Parietal                  | -                                               | Medium                              |
| **E44**       | 44           | -7.41  | 1.38   | -3.85  | Left Lateral-temporal border   | -                                               | Medium                              |
| **E45**       | 45           | -7.91  | -2.02  | -0.68  | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E46**       | 46           | -7.92  | -2.49  | 2.58   | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E47**       | 47           | -7.29  | -3.26  | 4.52   | Left Parietal                  | Left lateral/superior-temporal language-related | Medium                              |
| **E50**       | 50           | -7.34  | -4.36  | -0.25  | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E51**       | 51           | -7.10  | -5.05  | 2.98   | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E52**       | 52           | -6.31  | -4.87  | 5.37   | Left Parietal                  | -                                               | Medium                              |
| **E53**       | 53           | -4.54  | -4.37  | 7.56   | Left Parietal                  | -                                               | Medium                              |
| **E54**       | 54           | -2.46  | -3.70  | 8.88   | Left Parietal                  | -                                               | Medium                              |
| **E55**       | 55           | 0.00   | -2.32  | 9.52   | Midline Parietal (Cz stand-in) | -                                               | Medium                              |
| **E57**       | 57           | -7.12  | -4.05  | -3.24  | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E58**       | 58           | -6.53  | -6.23  | 0.06   | Left Lateral-temporal border   | Left lateral/superior-temporal language-related | Medium                              |
| **E59**       | 59           | -5.63  | -6.97  | 3.23   | Left Occipital                 | Left lateral/superior-temporal language-related | Medium                              |
| **E60**       | 60           | -4.46  | -6.56  | 5.81   | Left Parietal                  | -                                               | Medium                              |
| **E61**       | 61           | -2.54  | -5.93  | 7.64   | Left Parietal                  | -                                               | Medium                              |
| **Pz (E62)**  | 62           | 0.00   | -7.23  | 7.00   | Midline Parietal               | -                                               | High (nominal 10-10 correspondence) |
| **E64**       | 64           | -5.85  | -6.36  | -3.13  | Left Parietal                  | Left lateral/superior-temporal language-related | Medium                              |
| **E65**       | 65           | -5.03  | -7.88  | 0.14   | Left Occipital                 | Left lateral/superior-temporal language-related | Medium                              |
| **E66**       | 66           | -3.91  | -8.30  | 3.39   | Left Occipital                 | -                                               | Medium                              |
| **E67**       | 67           | -2.00  | -7.96  | 5.66   | Left Occipital                 | -                                               | Medium                              |
| **E69**       | 69           | -3.82  | -8.23  | -3.05  | Left Occipital                 | -                                               | Medium                              |
| **E70**       | 70           | -2.97  | -9.32  | 0.26   | Left Occipital                 | -                                               | Medium                              |
| **E71**       | 71           | -1.52  | -9.14  | 3.55   | Left Occipital                 | -                                               | Medium                              |
| **E72**       | 72           | 0.00   | -8.48  | 5.08   | Midline Occipital              | -                                               | Medium                              |
| **E74**       | 74           | -1.22  | -9.15  | -2.85  | Left Occipital                 | -                                               | Medium                              |
| **Oz (E75)**  | 75           | 0.00   | -9.74  | 0.53   | Midline Occipital              | -                                               | High (nominal 10-10 correspondence) |
| **E76**       | 76           | 1.52   | -9.14  | 3.55   | Right Occipital                | -                                               | Medium                              |
| **E77**       | 77           | 2.00   | -7.96  | 5.66   | Right Occipital                | -                                               | Medium                              |
| **E78**       | 78           | 2.54   | -5.93  | 7.64   | Right Parietal                 | -                                               | Medium                              |
| **E79**       | 79           | 2.46   | -3.70  | 8.88   | Right Parietal                 | -                                               | Medium                              |
| **E80**       | 80           | 2.12   | -0.74  | 9.27   | Right Central                  | -                                               | Medium                              |
| **E82**       | 82           | 1.22   | -9.15  | -2.85  | Right Occipital                | -                                               | Medium                              |
| **E83**       | 83           | 2.97   | -9.32  | 0.26   | Right Occipital                | -                                               | Medium                              |
| **E84**       | 84           | 3.91   | -8.30  | 3.39   | Right Occipital                | -                                               | Medium                              |
| **E85**       | 85           | 4.46   | -6.56  | 5.81   | Right Parietal                 | -                                               | Medium                              |
| **E86**       | 86           | 4.54   | -4.37  | 7.56   | Right Parietal                 | -                                               | Medium                              |
| **E87**       | 87           | 4.23   | -1.64  | 8.41   | Right Central                  | -                                               | Medium                              |
| **E89**       | 89           | 3.82   | -8.23  | -3.05  | Right Occipital                | -                                               | Medium                              |
| **E90**       | 90           | 5.03   | -7.88  | 0.14   | Right Occipital                | -                                               | Medium                              |
| **E91**       | 91           | 5.63   | -6.97  | 3.23   | Right Occipital                | -                                               | Medium                              |
| **E92**       | 92           | 6.31   | -4.87  | 5.37   | Right Parietal                 | -                                               | Medium                              |
| **E93**       | 93           | 6.45   | -2.53  | 6.50   | Right Parietal                 | -                                               | Medium                              |
| **E95**       | 95           | 5.85   | -6.36  | -3.13  | Right Parietal                 | -                                               | Medium                              |
| **E96**       | 96           | 6.53   | -6.23  | 0.06   | Right Lateral-temporal border  | -                                               | Medium                              |
| **E97**       | 97           | 7.10   | -5.05  | 2.98   | Right Lateral-temporal border  | -                                               | Medium                              |
| **E98**       | 98           | 7.29   | -3.26  | 4.52   | Right Parietal                 | -                                               | Medium                              |
| **E100**      | 100          | 7.12   | -4.05  | -3.24  | Right Lateral-temporal border  | -                                               | Medium                              |
| **E101**      | 101          | 7.34   | -4.36  | -0.25  | Right Lateral-temporal border  | -                                               | Medium                              |
| **E102**      | 102          | 7.92   | -2.49  | 2.58   | Right Lateral-temporal border  | -                                               | Medium                              |
| **E103**      | 103          | 7.48   | -0.87  | 4.98   | Right Central                  | -                                               | Medium                              |
| **C4 (E104)** | 104          | 5.93   | 0.31   | 6.91   | Right Central                  | -                                               | High (nominal 10-10 correspondence) |
| **E105**      | 105          | 4.00   | 1.04   | 8.26   | Right Central                  | Right inferior-frontal homolog                  | Medium                              |
| **E106**      | 106          | 1.33   | 1.69   | 9.14   | Right Central                  | -                                               | Medium                              |
| **E108**      | 108          | 7.91   | -2.02  | -0.68  | Right Lateral-temporal border  | -                                               | Medium                              |
| **E109**      | 109          | 8.00   | 0.03   | 2.32   | Right Lateral-temporal border  | -                                               | Medium                              |
| **E110**      | 110          | 6.94   | 1.61   | 5.13   | Right Central                  | Right inferior-frontal homolog                  | Medium                              |
| **E111**      | 111          | 5.16   | 2.92   | 6.82   | Right Central                  | Right inferior-frontal homolog                  | Medium                              |
| **E112**      | 112          | 2.64   | 3.52   | 8.24   | Right Frontal                  | -                                               | Medium                              |
| **E114**      | 114          | 7.41   | 1.38   | -3.85  | Right Lateral-temporal border  | -                                               | Medium                              |
| **E115**      | 115          | 7.79   | 0.92   | -0.96  | Right Lateral-temporal border  | -                                               | Medium                              |
| **E116**      | 116          | 7.39   | 3.21   | 2.63   | Right Lateral-temporal border  | Right inferior-frontal homolog                  | Medium                              |
| **E117**      | 117          | 6.01   | 4.50   | 5.01   | Right Frontal                  | Right inferior-frontal homolog                  | Medium                              |
| **E118**      | 118          | 4.14   | 5.55   | 6.43   | Right Frontal                  | Right inferior-frontal homolog                  | Medium                              |
| **E121**      | 121          | 7.09   | 3.91   | -3.63  | Right Lateral-temporal border  | -                                               | Medium                              |
| **E122**      | 122          | 6.93   | 4.47   | -0.39  | Right Lateral-temporal border  | Right inferior-frontal homolog                  | Medium                              |
| **E123**      | 123          | 6.15   | 5.90   | 3.07   | Right Frontal                  | Right inferior-frontal homolog                  | Medium                              |
| **E124**      | 124          | 4.83   | 6.52   | 4.73   | Right Frontal                  | Right inferior-frontal homolog                  | Medium                              |
