"""
Branding configuration system for multi-client dashboard customization.
Allows easy swapping of colors, logos, and client names.
"""

class ClientBranding:
    """
    Configurable branding for each client dashboard.
    Supports template-based themes with easy customization.
    """

    TEMPLATES = {
        'aux_default': {
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'accent_color': '#2ecc71',
            'warning_color': '#f39c12',
            'danger_color': '#e74c3c',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'background': '#f8f9fa',
            'logo_path': '/assets/logos/aux_insights.png',
            'client_name': 'AUX Insights',
            'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'font_family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
        },
        'client_template': {
            'primary_color': '#0066CC',
            'secondary_color': '#003D7A',
            'accent_color': '#FF6B35',
            'warning_color': '#FFB347',
            'danger_color': '#DC143C',
            'text_primary': '#1a1a1a',
            'text_secondary': '#666666',
            'background': '#ffffff',
            'logo_path': '/assets/logos/client_logo.png',
            'client_name': '{{CLIENT_NAME}}',
            'gradient': 'linear-gradient(135deg, #0066CC 0%, #003D7A 100%)',
            'font_family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
        },
        'dossier': {
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'accent_color': '#e74c3c',
            'warning_color': '#f39c12',
            'danger_color': '#c0392b',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'background': '#f8f9fa',
            'logo_path': '/assets/logos/aux_insights.png',
            'client_name': 'Dossier',
            'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'font_family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
        }
    }

    # Channel-specific colors for executive summary cards
    CHANNEL_COLORS = {
        'DTC Ecomm': {
            'bg': '#667eea',
            'accent': '#5568d3',
            'light': '#e8ebfc'
        },
        'Wholesale Retail': {
            'bg': '#f39c12',
            'accent': '#e67e22',
            'light': '#fef5e7'
        },
        'Marketplace': {
            'bg': '#2ecc71',
            'accent': '#27ae60',
            'light': '#e8f8f5'
        },
        'TikTok Shop': {
            'bg': '#e74c3c',
            'accent': '#c0392b',
            'light': '#fadbd8'
        }
    }

    @classmethod
    def get_theme(cls, template_name='aux_default'):
        """
        Return branding configuration for specified template.

        Args:
            template_name: str - Name of template ('aux_default', 'client_template', etc.)

        Returns:
            dict - Theme configuration with colors, logo, gradients
        """
        return cls.TEMPLATES.get(template_name, cls.TEMPLATES['aux_default'])

    @classmethod
    def customize(cls, template_name, **kwargs):
        """
        Create custom brand theme by overriding template values.

        Args:
            template_name: str - Base template to customize
            **kwargs: dict - Values to override (client_name, primary_color, etc.)

        Returns:
            dict - Customized theme configuration

        Example:
            theme = ClientBranding.customize(
                'client_template',
                client_name='Dossier',
                primary_color='#FF0066',
                logo_path='/assets/logos/dossier.png'
            )
        """
        base = cls.TEMPLATES[template_name].copy()
        base.update(kwargs)

        # Update gradient if primary/secondary colors changed
        if 'primary_color' in kwargs or 'secondary_color' in kwargs:
            primary = kwargs.get('primary_color', base['primary_color'])
            secondary = kwargs.get('secondary_color', base['secondary_color'])
            base['gradient'] = f'linear-gradient(135deg, {primary} 0%, {secondary} 100%)'

        return base

    @classmethod
    def get_channel_colors(cls, channel_name):
        """
        Get color scheme for a specific channel.

        Args:
            channel_name: str - Channel name ('DTC Ecomm', 'Wholesale Retail', etc.)

        Returns:
            dict - Color scheme with bg, accent, and light colors
        """
        return cls.CHANNEL_COLORS.get(channel_name, {
            'bg': '#95a5a6',
            'accent': '#7f8c8d',
            'light': '#ecf0f1'
        })

    @classmethod
    def generate_css_variables(cls, theme):
        """
        Generate CSS variables string from theme.

        Args:
            theme: dict - Theme configuration

        Returns:
            str - CSS :root variables
        """
        return f"""
        :root {{
            --primary-color: {theme['primary_color']};
            --secondary-color: {theme['secondary_color']};
            --accent-color: {theme['accent_color']};
            --warning-color: {theme['warning_color']};
            --danger-color: {theme['danger_color']};
            --text-primary: {theme['text_primary']};
            --text-secondary: {theme['text_secondary']};
            --background: {theme['background']};
            --gradient: {theme['gradient']};
            --font-family: {theme['font_family']};
        }}
        """
