class GridConfiguration:
    def __init__(self,
                 x_min, x_max, x_resolution,
                 theta_x_min, theta_x_max, theta_x_resolution,
                 y_min, y_max, y_resolution,
                 theta_y_min, theta_y_max, theta_y_resolution,
                 pt_min, pt_max, pt_resolution):
        self.x_min = x_min
        self.x_max = x_max
        self.x_resolution = x_resolution
        self.y_min = y_min
        self.y_max = y_max
        self.y_resolution = y_resolution
        self.theta_x_min = theta_x_min
        self.theta_x_max = theta_x_max
        self.theta_x_resolution = theta_x_resolution
        self.theta_y_min = theta_y_min
        self.theta_y_max = theta_y_max
        self.theta_y_resolution = theta_y_resolution
        self.pt_min = pt_min
        self.pt_max = pt_max
        self.pt_resolution = pt_resolution

    @staticmethod
    def from_sigma(x_mean, sigma_x, x_resolution,
                   theta_x_mean, sigma_theta_x, theta_x_resolution,
                   y_mean, sigma_y, y_resolution,
                   theta_y_mean, sigma_theta_y, theta_y_resolution,
                   pt_mean, sigma_pt, pt_resolution):
        return GridConfiguration(x_mean - sigma_x, x_mean + sigma_x, x_resolution,
                                 theta_x_mean - sigma_theta_x, theta_x_mean + sigma_theta_x, theta_x_resolution,
                                 y_mean - sigma_y, y_mean + sigma_y, y_resolution,
                                 theta_y_mean - sigma_theta_y, theta_y_mean + sigma_theta_y, theta_y_resolution,
                                 pt_mean - sigma_pt, pt_mean + sigma_pt, pt_resolution)

    def get_number_of_particles(self):
        number_of_particles = self.pt_resolution * self.theta_y_resolution * self.y_resolution * \
            self.x_resolution * self.theta_x_resolution
        return number_of_particles

    @staticmethod
    def get_configuration_from_xml(xml_root_configuration):
        xml_configuration = xml_root_configuration.attrib
        return GridConfiguration(
            float(xml_configuration["x_min"]), float(xml_configuration["x_max"]), 1,
            float(xml_configuration["theta_x_min"]), float(xml_configuration["theta_x_max"]), 1,
            float(xml_configuration["y_min"]), float(xml_configuration["y_max"]), 1,
            float(xml_configuration["theta_y_min"]), float(xml_configuration["theta_y_max"]), 1,
            float(xml_configuration["ksi_min"]), float(xml_configuration["ksi_max"]),
            int(xml_configuration["tot_entries_number"])
        )
