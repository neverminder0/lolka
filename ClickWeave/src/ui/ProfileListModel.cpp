#include "ProfileListModel.h"
#include "Profile.h"
#include <QDebug>

ProfileListModel::ProfileListModel(QObject *parent)
    : QAbstractListModel(parent)
{
}

int ProfileListModel::rowCount(const QModelIndex &parent) const
{
    Q_UNUSED(parent)
    return m_filteredProfiles.size();
}

QVariant ProfileListModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() >= m_filteredProfiles.size()) {
        return QVariant();
    }

    Profile* profile = m_filteredProfiles.at(index.row());
    if (!profile) {
        return QVariant();
    }

    switch (role) {
        case ProfileRole:
            return QVariant::fromValue(profile);
        case NameRole:
            return profile->name();
        case DescriptionRole:
            return profile->description();
        case EnabledRole:
            return profile->enabled();
        case LastRunRole:
            return profile->lastRun();
        case TotalRunsRole:
            return profile->totalRuns();
        case TotalClicksRole:
            return profile->totalClicks();
        case StepCountRole:
            return profile->stepCount();
        default:
            return QVariant();
    }
}

QHash<int, QByteArray> ProfileListModel::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[ProfileRole] = "profile";
    roles[NameRole] = "name";
    roles[DescriptionRole] = "description";
    roles[EnabledRole] = "enabled";
    roles[LastRunRole] = "lastRun";
    roles[TotalRunsRole] = "totalRuns";
    roles[TotalClicksRole] = "totalClicks";
    roles[StepCountRole] = "stepCount";
    return roles;
}

void ProfileListModel::addProfile(Profile* profile)
{
    if (!profile || m_profiles.contains(profile)) {
        return;
    }

    connect(profile, &Profile::nameChanged, this, &ProfileListModel::onProfileChanged);
    connect(profile, &Profile::descriptionChanged, this, &ProfileListModel::onProfileChanged);
    connect(profile, &Profile::enabledChanged, this, &ProfileListModel::onProfileChanged);
    connect(profile, &Profile::statisticsChanged, this, &ProfileListModel::onProfileChanged);
    connect(profile, &Profile::stepsChanged, this, &ProfileListModel::onProfileChanged);

    m_profiles.append(profile);
    applyFilter();
}

void ProfileListModel::removeProfile(Profile* profile)
{
    if (!profile) {
        return;
    }

    int index = m_profiles.indexOf(profile);
    if (index >= 0) {
        removeProfile(index);
    }
}

void ProfileListModel::removeProfile(int index)
{
    if (index < 0 || index >= m_profiles.size()) {
        return;
    }

    Profile* profile = m_profiles.at(index);
    
    // Find index in filtered list
    int filteredIndex = m_filteredProfiles.indexOf(profile);
    
    if (filteredIndex >= 0) {
        beginRemoveRows(QModelIndex(), filteredIndex, filteredIndex);
        m_filteredProfiles.removeAt(filteredIndex);
        endRemoveRows();
    }
    
    // Disconnect signals
    profile->disconnect(this);
    m_profiles.removeAt(index);
}

void ProfileListModel::clear()
{
    beginResetModel();
    
    for (Profile* profile : m_profiles) {
        profile->disconnect(this);
    }
    
    m_profiles.clear();
    m_filteredProfiles.clear();
    endResetModel();
}

Profile* ProfileListModel::profileAt(int index) const
{
    if (index < 0 || index >= m_filteredProfiles.size()) {
        return nullptr;
    }
    return m_filteredProfiles.at(index);
}

int ProfileListModel::indexOf(Profile* profile) const
{
    return m_filteredProfiles.indexOf(profile);
}

void ProfileListModel::setFilter(const QString& filter)
{
    if (m_filter != filter) {
        m_filter = filter;
        applyFilter();
    }
}

void ProfileListModel::refreshProfile(Profile* profile)
{
    int index = m_filteredProfiles.indexOf(profile);
    if (index >= 0) {
        QModelIndex modelIndex = createIndex(index, 0);
        emit dataChanged(modelIndex, modelIndex);
    }
}

void ProfileListModel::onProfileChanged()
{
    Profile* profile = qobject_cast<Profile*>(sender());
    if (profile) {
        refreshProfile(profile);
        // Re-apply filter in case the change affects filtering
        applyFilter();
    }
}

void ProfileListModel::applyFilter()
{
    beginResetModel();
    
    m_filteredProfiles.clear();
    
    for (Profile* profile : m_profiles) {
        bool matches = true;
        
        if (!m_filter.isEmpty()) {
            QString lowerFilter = m_filter.toLower();
            matches = profile->name().toLower().contains(lowerFilter) ||
                     profile->description().toLower().contains(lowerFilter);
        }
        
        if (matches) {
            m_filteredProfiles.append(profile);
        }
    }
    
    endResetModel();
}