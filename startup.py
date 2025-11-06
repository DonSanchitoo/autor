import ctypes
import os
import configparser
from qgis.core import QgsApplication 
from qgis.PyQt.QtCore import QObject, QEvent, Qt, QTimer
from qgis.PyQt.QtGui import QFont, QIcon
from qgis.PyQt.QtWidgets import (
    QApplication, QTreeView, QDockWidget, QWidget, QLabel, 
    QVBoxLayout, QToolBar, QAction, QMainWindow, QMenu, QLineEdit
)
from qgis.PyQt.QtWidgets import (
    QApplication, QTreeView, QDockWidget, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QToolBar, QAction, QMainWindow, QMenu, QLineEdit
)

from qgis.utils import iface

# --- Vérifier si les touches M et E sont maintenues au démarrage (Windows) ---
VK_M = 0x4D
VK_E = 0x45

def is_key_pressed(vk_code):
    """Vérifie l'état d'une touche Windows."""
    return ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000 != 0

# --- Chemin relatif vers QGIS3.ini (fonctionne pour n'importe quel utilisateur) ---
qgis_appdata = os.path.join(os.getenv('APPDATA'), 'QGIS', 'QGIS3')
ini_path = os.path.join(qgis_appdata, 'profiles', 'default', 'QGIS', 'QGIS3.ini')

def set_processing(enabled: bool):
    """
    Active ou désactive Processing dans QGIS3.ini.
    enabled=True → processing activé
    enabled=False → processing désactivé
    """
    if not os.path.exists(ini_path):
        print(f"Fichier INI introuvable : {ini_path}")
        return

    config = configparser.ConfigParser()
    config.optionxform = str  # Respecte la casse des clés
    config.read(ini_path)

    section = "PythonPlugins"
    if section not in config.sections():
        config.add_section(section)

    # Modifier uniquement la clé 'processing'
    config.set(section, 'processing', 'true' if enabled else 'false')

    with open(ini_path, 'w') as f:
        config.write(f)

    print(f"Processing {'activé' if enabled else 'désactivé'} dans QGIS3.ini (au prochain démarrage).")

# ----------------------------------------------------------------------
# --- DÉFINITION DE LA FONCTION DE RESTAURATION (Mode Maintenance) ---
# ----------------------------------------------------------------------

def restaurer_interface_par_defaut():
    """
    Restaure l'interface QGIS en Mode Maintenance (E+M), en affichant
    tous les menus et barres d'outils, mais SEULEMENT les docks Couches et Explorateur.
    """
    print("Restauration de l'interface QGIS par défaut forcée (via PyQt).")
    
    mw = iface.mainWindow()
    docks_a_conserver = ['Layers', 'Browser']
    
    try:
        # 2. Rendre visibles TOUTES les barres d'outils
        for toolbar in mw.findChildren(QToolBar):
            toolbar.setVisible(True)
             
        # 3. Rendre visibles SEULEMENT les docks Couches et Explorateur
        for dock in mw.findChildren(QDockWidget):
            dock_name = dock.objectName()
            dock.setVisible(False)
            if dock_name in docks_a_conserver:
                dock.setVisible(True)
             
        # 4. Rendre visible la barre d'état
        mw.statusBar().setVisible(True)
        
        # 5. Rendre visibles tous les menus principaux
        menus_principaux = [
            'mProjectMenu', 'mEditMenu', 'mViewMenu', 'mLayerMenu', 
            'mSettingsMenu', 'mDatabaseMenu', 'mPluginMenu', 
            'mVectorMenu', 'mRasterMenu', 'mMeshMenu', 'mHelpMenu', 
            'mProcessingMenu', 'WebMenu'
        ]
        for name in menus_principaux:
            menu = mw.findChild(QMenu, name)
            if menu:
                menu.menuAction().setVisible(True)

        # Réactiver Processing dans QGIS3.ini pour M+E
        set_processing(True)

        iface.messageBar().pushInfo("Démarrage", "Mode administrateur - service Géomatique - E.SI")

    except Exception as e:
        iface.messageBar().pushWarning("Restauration Échouée", f"Impossible de restaurer l'interface: {e}")

# ----------------------------------------------------------------------
# --- LOGIQUE DE DÉMARRAGE CONDITIONNEL ---
# ----------------------------------------------------------------------

if is_key_pressed(VK_M) and is_key_pressed(VK_E):
    # --- Mode Maintenance ---
    print("Touches M + E enfoncées : mode Maintenance actif. Script de personnalisation ignoré.")
    
    from qgis.PyQt.QtGui import QPixmap, QFont
    from qgis.PyQt.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QApplication
    from qgis.PyQt.QtCore import Qt, QTimer
    import os

    # --- Splash screen ---
    splash = QWidget()
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
    splash.setAttribute(Qt.WA_TranslucentBackground)

    layout = QHBoxLayout()
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)

    # --- Logo ---
    script_dir = os.path.dirname(__file__)
    logo_path = os.path.join(script_dir, "logo.png")
    if os.path.exists(logo_path):
        logo_label = QLabel()
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(192, 192, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # logo raisonnable
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # ne s'étire pas
        layout.addWidget(logo_label)

    # --- Texte avec cadre serré autour du texte ---
    label = QLabel("Bienvenue dans QGIS for Administrator")
    label.setFont(QFont("Arial", 12, QFont.Bold))
    label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    label.setStyleSheet(
        "color: white;"
        "background-color: rgba(244, 44, 7, 1);"
        "border-radius: 8px;"
        "padding: 4px 8px;"  # fond proche du texte
    )
    label.setWordWrap(False)
    label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)  # taille minimale selon le texte

    layout.addWidget(label, 0)

    splash.setLayout(layout)

    # Laisser le widget choisir sa taille d'après son contenu
    splash.adjustSize()

    # --- Positionnement au centre de l'écran ---
    screen_geometry = QApplication.instance().primaryScreen().geometry()
    center_point = screen_geometry.center() - splash.rect().center()
    offset_y = 160
    splash.move(center_point.x(), center_point.y() + offset_y)
    splash.show()
    QTimer.singleShot(2500, splash.close)


    
    iface.initializationCompleted.connect(restaurer_interface_par_defaut)

else:
    # --- Mode Normal ---
    
    # Désactiver Processing dans QGIS3.ini pour le prochain démarrage
    set_processing(False)

    def masquer_tout_sauf_edition_selection():
        """
        Applique la personnalisation minimale (masque tout sauf Couches, Édition, Sélection).
        """
        mw = iface.mainWindow()

        # 0. Masquer la barre de menu ENTIÈRE
        mw.menuBar().setVisible(False)

        # 1. Masquer tous les panneaux/Docks par défaut (sauf 'Layers')
        docks_a_masquer = [
            'Browser', 'ResultsLog', 'ProcessingToolbox', 
            'mLayoutDock', 'LegendDock', 'mLayerStylingDock'
        ]
        for name in docks_a_masquer:
            dock = mw.findChild(QDockWidget, name)
            if dock:
                dock.setVisible(False)
                
        # 2. Supprimer la barre de recherche du panneau Explorateur (Browser)
        browser_dock = mw.findChild(QDockWidget, 'Browser')
        if browser_dock:
            search_bar = browser_dock.findChild(QLineEdit, 'mSearchLineEdit')
            if search_bar:
                search_bar.setVisible(False)

        # 3. Désactiver l'accès au Traitement (Bouton Boîte à outils)
        action_toolbox = mw.findChild(QAction, 'mActionOpenToolbox')
        if action_toolbox:
            action_toolbox.setVisible(False)
            
        # 4. Masquer TOUTES les barres d'outils Sauf Édition et Sélection
        all_toolbars = mw.findChildren(QToolBar)
        toolbars_a_conserver = [
            'mDigitizeToolBar',
            'mMapToolBar', 'mFileToolBar', 'mSelectionToolBar','mAdvancedDigitizeToolBar', 'mWebToolBar','mMapNavToolBar','mPluginToolBar'     
        ]
        status_bar = mw.statusBar()
        for child in status_bar.findChildren(QWidget):
            if child.objectName() == "LocatorWidget":
                child.setVisible(False)
        
        for toolbar in all_toolbars:
            toolbar.setVisible(False) 
            if toolbar.objectName() in toolbars_a_conserver:
                toolbar.setVisible(True)
        
        print("Interface utilisateur simplifiée : personnalisation appliquée.")
        iface.messageBar().pushSuccess("Personnalisation", "Interface simplifiée appliquée.")
        
    # --- Bouton table attributaire ---
    def ouvrir_table_attributaire_couche_selectionnee():
        couche = iface.layerTreeView().currentLayer()
        if couche:
            iface.showAttributeTable(couche)
        else:
            iface.messageBar().pushWarning("Table attributaire", "Aucune couche sélectionnée.")

    action_table = QAction(QIcon(), "Ouvrir la table attributaire", iface.mainWindow())
    action_table.setToolTip("Ouvre la table attributaire de la couche sélectionnée")
    action_table.triggered.connect(ouvrir_table_attributaire_couche_selectionnee)

    toolbar = iface.mainWindow().findChild(QToolBar, 'mSelectionToolBar')
    if toolbar:
        toolbar.addAction(action_table)
    else:
        nouvelle_toolbar = QToolBar("Table Attributaire")
        nouvelle_toolbar.addAction(action_table)
        iface.mainWindow().addToolBar(nouvelle_toolbar)

    from qgis.PyQt.QtGui import QPixmap, QFont
    from qgis.PyQt.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QApplication
    from qgis.PyQt.QtCore import Qt, QTimer
    import os

    # --- Splash screen ---
    splash = QWidget()
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
    splash.setAttribute(Qt.WA_TranslucentBackground)

    layout = QHBoxLayout()
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)

    # --- Logo ---
    script_dir = os.path.dirname(__file__)
    logo_path = os.path.join(script_dir, "logo.png")
    if os.path.exists(logo_path):
        logo_label = QLabel()
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(192, 192, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # logo raisonnable
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # ne s'étire pas
        layout.addWidget(logo_label)

    # --- Texte avec cadre serré autour du texte ---
    label = QLabel("Bienvenue dans QGIS for Capelle Group : Autor")
    label.setFont(QFont("Arial", 12, QFont.Bold))
    label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    label.setStyleSheet(
        "color: white;"
        "background-color: rgba(46, 52, 64, 220);"
        "border-radius: 8px;"
        "padding: 4px 8px;"  # fond proche du texte
    )
    label.setWordWrap(False)
    label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)  # taille minimale selon le texte

    layout.addWidget(label, 0)

    splash.setLayout(layout)

    # Laisser le widget choisir sa taille d'après son contenu
    splash.adjustSize()

    # --- Positionnement au centre de l'écran ---
    screen_geometry = QApplication.instance().primaryScreen().geometry()
    center_point = screen_geometry.center() - splash.rect().center()
    offset_y = 160
    splash.move(center_point.x(), center_point.y() + offset_y)
    splash.show()
    QTimer.singleShot(2500, splash.close)

    # --- Filtre clic droit et double-clic ---
    class BlockMouseEvents(QObject):
        def eventFilter(self, obj, event):
            if event.type() == QEvent.MouseButtonPress and event.button() == 2:
                return True
            if event.type() == QEvent.MouseButtonDblClick:
                parent = obj.parent()
                while parent:
                    if isinstance(parent, QDockWidget) and "Couches" in parent.windowTitle():
                        return True
                    parent = parent.parent()
            return super().eventFilter(obj, event)

    filter = BlockMouseEvents()
    QApplication.instance().installEventFilter(filter)

    # --- Connexion de la Personnalisation au démarrage de QGIS ---
    iface.initializationCompleted.connect(masquer_tout_sauf_edition_selection)
