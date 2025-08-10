#pragma once

#include <QAbstractListModel>
#include <QList>

class Profile;

class ProfileListModel : public QAbstractListModel
{
    Q_OBJECT

public:
    enum ProfileRoles {
        ProfileRole = Qt::UserRole + 1,
        NameRole,
        DescriptionRole,
        EnabledRole,
        LastRunRole,
        TotalRunsRole,
        TotalClicksRole,
        StepCountRole
    };

    explicit ProfileListModel(QObject *parent = nullptr);

    // QAbstractListModel interface
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

    // Custom methods
    void addProfile(Profile* profile);
    void removeProfile(Profile* profile);
    void removeProfile(int index);
    void clear();
    
    Profile* profileAt(int index) const;
    int indexOf(Profile* profile) const;
    
    void setFilter(const QString& filter);
    void refreshProfile(Profile* profile);

private slots:
    void onProfileChanged();

private:
    void applyFilter();

private:
    QList<Profile*> m_profiles;
    QList<Profile*> m_filteredProfiles;
    QString m_filter;
};